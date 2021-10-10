import sys
sys.path.append("..")

import emach.tools.jmag as jd

tool_jmag = jd.JmagDesigner()
file = r'one.jproj'
tool_jmag.open(filepath=file)