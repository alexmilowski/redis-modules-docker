import sys
import argparse
import yaml

parser = argparse.ArgumentParser(description="Redis module dockerfile generator")
parser.add_argument('--baseimage',help='The base image for the target',default='redis:latest')
parser.add_argument('--exclude',help='a module to exclude',action='append')
parser.add_argument('--module-image',help='a module image override',nargs=2,action='append')
parser.add_argument('--libdir',help='the libdir for modules',default='$REDIS_MODULES/')
parser.add_argument('--output',help='An output file for the result')
parser.add_argument('--expose',help='The port to expose',type=int,default=6379)
parser.add_argument('files',nargs='*',help='A module files (YAML format)')

args = parser.parse_args()

if len(args.files)==0:
   args.files = [('stdin',sys.stdin)]

if args.exclude is None:
   exclusions = set()
else:
   exclusions = set(args.exclude)

sources = {}

module_images = {}
if args.module_image is not None:
   for module,image in args.module_image:
      module_images[module] = image

target_script = """ENV REDIS_MODULES /opt/redislabs/lib/modules
RUN mkdir -p $REDIS_MODULES/
WORKDIR /data
"""

if args.output is None:
   output = sys.stdout
else:
   output = open(args.output,'r')

def error(message,*args,**keywords):
   sys.stderr.write(message.format(*args,**keywords))
   sys.stderr.write('\n')

def quit(message,*args,**keywords):
   error(message,*args,**keywords)
   sys.exit(1)

def load_modules(source,target,*module_list):
   for index, module in enumerate(module_list):
      name = module.get('name',None)
      if not name:
         error('Ignoring unnamed module at position {} in {}',index,source)
         continue
      if name in exclusions:
         continue
      image = module_images.get(name,module.get('image',None))
      if image is None:
         quit('Missing image for module {}',name)
      module['image'] = image
      target[name] = module

for spec_source in args.files:
   if type(spec_source)==str:
      with open(spec_source) as file:
         spec = yaml.load(file,Loader=yaml.Loader)
   else:
      spec = yaml.load(spec_source[1],Loader=yaml.Loader)
      spec_source = spec_source[0]
   if type(spec)==list:
      load_modules(spec_source,sources,*spec)
   elif type(spec)==dict and spec.get('kind',None)=='Module':
      load_modules(spec_source,sources,spec)
   elif type(spec)==dict and spec.get('kind',None)=='Target':
      args.baseimage = spec.get('baseimage',args.baseimage)
      args.expose = int(spec.get('expose',args.expose))
      target_script = spec.get('script',target_script)
      args.libdir = spec.get('libdir',args.libdir)
      load_modules(spec_source,sources,*spec.get('modules',[]))
   else:
      error('Ignoring top-level that is not a target, module, or array of modules.')

for _, (name, module) in enumerate(sources.items()):
   image = module.get('image',None)
   if image is None:
      quit('Missing image for module {}',name)
   output.write('FROM {image} as {name}\n'.format(**module))

output.write("""
# Target image
FROM {baseimage}
""".format(baseimage=args.baseimage))
output.write(target_script)
output.write('\n')

for _, (name, module) in enumerate(sources.items()):
   output.write('# {} module\n'.format(name))
   if 'script' in module:
      output.write(module['script'])
   for index,artifact in enumerate(module.get('artifacts',[])):
      source = artifact.get('source',None)
      if source is None:
         quit('Artifact {} in {} is missing a source.',index,name)
      target = artifact.get('target',args.libdir)
      chown = '--chown={}'.format(artifact['user']) if 'user' in artifact else ''
      output.write('COPY --from={name} {chown} "{source}" "{target}"\n'.format(name=name,chown=chown,source=source,target=target))
   output.write('\n')

output.write('EXPOSE {port}\n'.format(port=str(args.expose)))

output.write('CMD [')
separator = ' '

for _, (name, module) in enumerate(sources.items()):
   for command in module.get('command',[]):
      output.write(separator)
      output.write('"')
      output.write(command)
      output.write('"')
      separator = ', '

output.write(' ]\n')

if args.output is not None:
   output.close()
