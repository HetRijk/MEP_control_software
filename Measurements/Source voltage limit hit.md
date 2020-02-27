# Source voltage limit hit?

If the SMU has to apply too much voltage in order to get a certain source current, a limit may be hit causing the system to go into compliance state and thereby somehow increasing its resistance

This could be happening when the device voltage measured exceeds 1.5V and therefore be the cause of the kinks seen in the IV curves

- Voltage cannot be measured by regular multimeter due to extremely high device resistance
- Measured by 2-point resistance across current contacts
	- Slightly below 8V for 50 nA source current
- Manual:
	- For source currents below 100 nA, the voltage limit is 210 V

So it looks like this is not the explanation for the IV curve kink