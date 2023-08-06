# GELUBackprop {#dev_guide_op_gelubackprop}

**Versioned name**: *GELUBackprop-1*

**Category**: *Activation*

**Short description**: *GELUBackprop* computes gradient for GELU.

## Inputs

* **1**: ``input_forward`` - original input tensor of GELU op. **Required.**

  * **Type**: T

* **2**: ``output_delta`` - the gradient tensor with respect to the output of
  GELU. **Required.**

  * **Type**: T

## Outputs

* **1**: ``input_delta`` - the gradient tensor with respect to the input of
  GELU.

  * **Type**: T

**Types**:

* **T**: f32, f16, bf16.
* **Note**: Inputs and outputs have the same data type denoted by *T*. For
  example, if input is f32 tensor, then all other tensors have f32 data type.
