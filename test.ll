define float @test(float %v) {
  %ret = call float @llvm.trunc.f32(float %v)
  ret float %ret
}
