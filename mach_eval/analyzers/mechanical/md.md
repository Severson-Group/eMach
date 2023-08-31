# Summary
This PR adds SPM speed limit code to eMach code base.

# Mass and Stiffness
BP5 was used in determining the mass and unstable stiffness value. The $k_{\delta}$ value for BP5 is `193.39e3 N-m`. Assume an unstable pole of 50Hz, the allowable rotor mass is determined to be `1.9595 kg`.

# Control Tuning and Bode Plot
Given the current regulator behaves like a first order low pass filter with a 1.5kHz bandwidth, using the frequency design method for the mag bearing controller, the PID gains are determined as follow:

$K_p = 3.5575 \times 10^{5}$
$K_i =3.1747 \times 10^{6}$
$K_d= 2.0009 \times 10^{3}$

The bandwidth chosen is 150Hz, which is 10x lower than the current regulator for good separation. The zero of the controller is placed at 1.5Hz (100x lower than bandwidth) and the pole is placed at 600Hz (4x higher than bandwidth). Phase margin is selected to be $\phi_{pm} = \pi/3$ for good practice. 

The bode plot is obtained and shown below. 
![image](https://user-images.githubusercontent.com/66574308/229968640-9db71358-cd8d-4c14-b63d-6bc43ea1c7a8.png)

# Simulation
Simulink model
![image](https://user-images.githubusercontent.com/66574308/231320255-6fd8c33b-3d65-4f80-9e60-fedea88fd82c.png)

Scenario 1 - shaft fully displaced initially.
![case1](https://user-images.githubusercontent.com/66574308/231320202-41ca5eaf-70ec-4416-afa9-04713c8e89e5.png)

Scenario 2 - shaft initially centered and at 0.1s an impulse disturbance force applied onto the shaft . The magnitude of the impulse is 10x rotor mass. (192.22N)
![case2](https://user-images.githubusercontent.com/66574308/231320208-3a3a50dd-00d4-4404-aa7b-b723756756a8.png)


