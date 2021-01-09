from dim_millimeter import DimMillimeter
from dim_inch import DimInch

from dim_degree import DimDegree
from dim_radian import DimRadian

inchObject = DimInch(1)
milObject = DimMillimeter(25.4)

print('***********ADD Demo*************')
print('Adding Inch + Millimeter objects')
print(inchObject+milObject)
print(type(inchObject+milObject))
print('Adding Millimeter + Inch objects')
print(milObject+inchObject)
print(type(milObject+inchObject))



print('**********SUB Demo**************')
print('Subracting Inch - Millimeter object')
print(inchObject-milObject)
print(type(inchObject-milObject))
print('Subracting Millimeter - Inch Object')
print(milObject-inchObject)
print(type(milObject-inchObject))
#
print('*********Multiply Demo**********')
print('Multiplying Inch * int object')
print(inchObject*5)
print(type(inchObject*5))
print('Multiplying int * Inch object')
print(5*inchObject)
print(type(5*inchObject))
#
print('Multiplying Inch * float object')
print(inchObject*5.58)
print(type(inchObject*5.58))
print('Multiplying float * Inch object')
print(5.58*inchObject)
print(type(5.58*inchObject))

print('Multiplying Millimeter * int object')
print(milObject*5)
print(type(milObject*5))
print('Multiplying int * Inch object')
print(5*milObject)
print(type(5*milObject))

print('Multiplying Millimeter * float object')
print(milObject*5.58)
print(type(milObject*5.58))
print('Multiplying float * Inch object')
print(5.58*milObject)
print(type(5.58*milObject))



print('*********Divide Demo**********')
print('Dividing inch object with mil object')
print(inchObject/milObject)
print(type(inchObject/milObject))
print('Dividing inch object by scalar')
print(inchObject*5)
print(type(inchObject*5))
# print('Dividing scalar object by inch object')
# print(5/inchObject)
# print(type(inchObject/5))

print('*******Angle Demo******')
degObject = DimDegree(180)
print(type(degObject))
print(DimRadian(degObject))

radObject = DimRadian(3.14)
print(type(radObject))
print(DimDegree(radObject))

print('Angle Unary operation')
print(-degObject)













