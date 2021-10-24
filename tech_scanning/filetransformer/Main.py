from TextExtract import *
from EngPreprocess import *

my_text_path = "C:/Users/wonai/mystatus/Doit_program/tech_scanning/filetransformer/practice.hwp"

##te = TextExtract(my_text_path)
epp = EngPreprocess(my_text_path)
print(epp.propressing())