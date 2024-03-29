import os
import sys

# change current working directory to file location
os.chdir(os.path.dirname(__file__))
# add the directory immediately above this file's directory to path for module import
sys.path.append("../..")

from mach_cad.model_obj import DimMillimeter, DimInch, DimDegree, DimRadian

inchObject = DimInch(5)
milObject = DimMillimeter(20)

# print('***********ADD Demo*************')
print("Adding Inch + Millimeter objects")
print(inchObject)
print(inchObject + milObject)
print(type(inchObject + milObject))
print("Adding Millimeter + Inch objects")
print(milObject + inchObject)
print(type(milObject + inchObject))

print("**********SUB Demo**************")
print("Subtracting Inch - Millimeter object")
print(inchObject - milObject)
print(type(inchObject - milObject))
print("Subtracting Millimeter - Inch Object")
print(milObject - inchObject)
print(type(milObject - inchObject))

print("*********Multiply Demo**********")
print("Multiplying Inch * int object")
print(inchObject * 5)
print(type(inchObject * 5))
print("Multiplying int * Inch object")
print(5 * inchObject)
print(type(5 * inchObject))

print("Multiplying Inch * float object")
print(inchObject * 5.58)
print(type(inchObject * 5.58))
print("Multiplying float * Inch object")
print(5.58 * inchObject)
print(type(5.58 * inchObject))

print("Multiplying Millimeter * int object")
print(milObject * 5)
print(type(milObject * 5))
print("Multiplying int * Millimeter object")
print(5 * milObject)
print(type(5 * milObject))

print("Multiplying Millimeter * float object")
print(milObject * 5.58)
print(type(milObject * 5.58))
print("Multiplying float * Inch object")
print(5.58 * milObject)
print(type(5.58 * milObject))

print("*********Divide Demo**********")
print("Dividing inch object with mil object")
print(inchObject / milObject)
print(type(inchObject / milObject))
print("Dividing inch object by scalar")
print(inchObject / 5)
print(type(inchObject / 5))

# ###### Uncomment this to check exception #######
# # print('Dividing scalar object by inch object')
# # print(5/inchObject)
# # print(type(inchObject/5))

###### Uncomment this to check exception #######
# print('********Power Demo*****')
# print(inchObject**2)
# print(2**inchObject)
# print(inchObject**milObject)

print("*******Angle Demo******")
degObject = DimDegree(180)
print(type(degObject))

radObject = DimRadian(3.14)
print(type(radObject))

print("Angle Unary operation")
print(-degObject)
negDegObject = DimDegree(-180)
print(-negDegObject)

print("******Nested Dimension Demo*********")
print("DimMillimeter(inchObject)")
print(DimMillimeter(inchObject))
print(type(DimMillimeter(inchObject)))
print("DimInch(milObject)")
print(DimInch(milObject))
print(type(DimInch(milObject)))
print("DimRadian(degObject)")
print(DimRadian(degObject))
print(type(DimRadian(degObject)))
print("DimDegree(radObject)")
print(DimDegree(radObject))
print(type(DimDegree(radObject)))
