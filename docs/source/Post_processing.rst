4. Post-Processing the acquired data
************************************

Theory
======

The Rabi frequency is proportional to the square root of the Intensity. Let's write this relation as :math:`\Omega = A \sqrt{I}`.
Let's assume we know :math:`\Omega` for a RF amplitude :math:`V_0`, and write this Rabi frequency :math:`\Omega_0`.
Using our setup, we measure :math:`I_0 = I(V_0)`, and deduce :math:`A = \frac{\Omega_0}{I_0}`.
Therefore we now have :math:`\Omega^2(V) = \frac{\Omega^2_0}{I^2_0} I(V)`.
:math:`V` is obtained from :math:`\Omega^2` as :math:`V(\Omega) = I^{-1}(\frac{I^2_0}{\Omega^2_0} \Omega^2)`.

Implementation
==============
The core of the problem is about building the inverse function of the intensity :math:`I^{-1}`, that takes an intensity and outputs a voltage.
From the output of the previous simulation, we have two arrays of data associating intensities `i` to voltage `a`. The function looks like a bijection, and it also makes sense to plot the voltage `a` function of the intensity `i`.
This disrete `V(I)` set of points can be interpolated using :py:func:`scipy.interpolate.interp1d`, building the wanted :math:`V = I^{-1}(I)` curve. Note that lots of points are necessary in the zones where the I(V) is almost constant (for small amplitudes for example).

To find the RF amplitude associated to a Rabi frequency, you then just have to call the interpolated function just built with parameter :math:`\frac{I^2_0}{\Omega^2_0} \Omega^2(V)`  
