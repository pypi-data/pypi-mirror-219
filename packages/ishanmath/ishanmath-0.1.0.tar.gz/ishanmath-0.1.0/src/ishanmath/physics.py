from numbers import Number
from exceptions import IshanMathException

l_unit = ["m", "cm"]

class Calculate:
    def __init__(self) -> None:
        pass

    def area(self, length: Number, breadth: Number):
        """
        Returns the area of a figure.

        Area is the product of length and breadth taken as input
        """
        return length*breadth
    
    
    def volume(self, length: Number, breadth: Number, height: Number):
        """
        Returns the volume of a figure.

        Volume is the product of length, breadth and height taken as input
        """
        return length*breadth*height
    
    
    def density(self, mass: Number, volume: Number):
        """
        Returns the density of an object.

        Density of an object is its mass per unit area.

        Mass and volume are taken as input
        """
        return mass/volume
    
    
    def speed(self, distance: Number, time: Number):
        """
        Returns the speed of a body.

        Speed of a body is the distance travelled by it per unit time

        Distance and time are taken as input
        """
        return distance/time
    
    
    def velocity(self, displacement: Number, time: Number):
        """
        Returns the velocity of a body.

        Velocity of a body is the distance travelled by it per unit time in a specified direction

        Displacement and time are taken as input
        """
        return displacement/time
    
    
    def acceleration(self, *values:Number, **kvalues):
        """
        Returns the acceleration of a body.

        Acceleration of a body is the rate of change of velocity per unit time

        Velocity and time are taken as input
        """
        if values and kvalues:
            raise IshanMathException("All", "Args and kwargs can't be used together")
        if values:
            if len(values) == 2:
                return values[0]/values[1]
            elif len(values) == 3:
                return (values[1]-values[0])/values[2]
            else:
                raise IshanMathException("All", "Invalid number of fields")
        if kvalues:
            vals = kvalues.items()
            if len(vals) == 2:
                try:
                    return kvalues["v"]/kvalues["t"]
                except:
                    try:
                        return kvalues["velocity"]/kvalues["time"]
                    except:
                        raise IshanMathException("All", "Invalid fields")
            elif len(vals) == 3:
                try:
                    return (kvalues["v"]-kvalues["u"])/kvalues["t"]
                except:
                    try:
                        return (kvalues["final_velocity"]-kvalues["initial_velocity"])/kvalues["time"]
                    except:
                        raise IshanMathException("All", "Invalid fields")
            else:
                raise IshanMathException("All", "Invalid number of fields")
            
            
    def force(self, mass: Number, acceleration: Number):
        """
        Returns the force acting on a body.

        Force is that physical cause which changes or tends to change either the size or the shape or the state of rest or motion of the body.

        Mass and acceleration are taken as input
        """
        return mass*acceleration
    
    
    def energy(self, force: Number, displacement: Number):
        """
        Returns the energy or work done by a body.

        Energy or work done is the product of force and displacement.

        Force and displacement are taken as input
        """
        return force*displacement
    
    
    def momentum(self, mass: Number, velocity: Number):
        """
        Returns the momentum a body.

        Momentum is the product of mass and velocity.

        Mass and Velocity are taken as input
        """
        return mass*velocity
    
    
    def torque(self, force: Number, distance: Number):
        return force*distance
    
    
    def power(self, work: Number, time: Number):
        return work/time
    
    
    def pressure(self, force: Number, area: Number):
        """
        Returns the pressure exerted by a body.

        Pressure is the force exerted by a body per unit area.

        Force and area are taken as input.
        """
        return force/area
    
    
    def frequency(self, time_period: Number):
        """
        Returns the frequency of oscillation of a body.

        Frequency is the number of oscillations made in 1 second.

        Time period is taken as input.
        """
        return 1/time_period
    

    def frequency(self, time_period: Number):
        """
        Returns the time period of an oscillating body.

        Time period is the time taken to complete one oscillation.

        Time period is taken as input.
        """
        return 1/time_period
    
    
    def electric_charge(self, current: Number, time: Number):
        return current*time
    
    
    def emf(self, work: Number, charge: Number):
        return work/charge
    
    
    def electrical_resistance(self, potential: Number, current: Number):
        return potential/current
    
    
    def electrical_power(self, potential: Number, current: Number):
        return potential*current
        
Calculate.force()
