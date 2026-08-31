import ctypes, os, sys
sys.path.append(os.path.abspath('tinygrad_repo'))
from tinygrad.runtime.autogen import llvm

llvm.LLVMInitializeX86TargetInfo()
llvm.LLVMInitializeX86Target()
llvm.LLVMInitializeX86TargetMC()
llvm.LLVMInitializeX86AsmPrinter()

def test_ir(ir):
    ctx = llvm.LLVMContextCreate()
    src_buf = llvm.LLVMCreateMemoryBufferWithMemoryRangeCopy(ir.encode(), len(ir), b"")
    err = ctypes.POINTER(ctypes.c_char)()
    m = llvm.LLVMModuleRef()
    res = llvm.LLVMParseIRInContext(ctx, src_buf, ctypes.pointer(m), ctypes.pointer(err))
    if res:
        print("ERROR:", ctypes.cast(err, ctypes.c_char_p).value.decode())
    else:
        print("SUCCESS")
    llvm.LLVMContextDispose(ctx)

print("Testing trunc...")
test_ir("""
declare float @llvm.trunc.f32(float)
define float @test(float %v) {
  %ret = call float @llvm.trunc.f32(float %v)
  ret float %ret
}
""")

print("Testing exp2...")
test_ir("""
define float @test(float %v) {
  %ret = call float @llvm.exp2.f32(float %v)
  ret float %ret
}
""")
