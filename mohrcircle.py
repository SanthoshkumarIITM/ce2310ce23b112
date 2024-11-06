
import math
import matplotlib.pyplot as plt
from matplotlib.patches import Circle 
from matplotlib.patches import Arc
import numpy as np
from tkinter import *
class strain:
      def __init__(self):
         

         x_normal_strain=float(input("Enter Normal strain in x-direction  : "))
         y_normal_strain=float(input("Enter Normal strain in y-direction : "))
         shear_gamma_strain=float(input("Enter shear strain on right face : "))
         shear_strain = shear_gamma_strain/2

         mohr_centre=(x_normal_strain+y_normal_strain)/2
         mohr_radius=((((x_normal_strain-y_normal_strain)/2)**2)+((shear_strain)**2))**0.5

         ps_angle1=0.5*math.atan((2*shear_strain)/(x_normal_strain-y_normal_strain))
         ps_angle2=ps_angle1+0.5*(math.pi)

         exshear_angle2=0.5*math.atan((x_normal_strain-y_normal_strain)/((-2)*shear_strain))
         exshear_angle1=exshear_angle2+0.5*(math.pi)

         shear_strain1=mohr_radius
         shear_strain2=-mohr_radius

         principal_strain1=((x_normal_strain+y_normal_strain)/2)+mohr_radius
         principal_strain2=((x_normal_strain+y_normal_strain)/2)-mohr_radius


         def onclick():
            pass

         root = Tk()
         text = Text(root)
         text.insert(INSERT, "Maximum Principal Strain = ")
         text.insert(END, principal_strain1)
         text.insert(INSERT, " ue \nMinimum Principal Strain = ")
         text.insert(END, principal_strain2)
         text.insert(INSERT, " ue \nMaximum Extreme Shear Strain = ")
         text.insert(END, 2*shear_strain1)
         text.insert(INSERT, " ue \nMinimum Extreme Shear Strain = ")
         text.insert(END, 2*shear_strain2)
         text.insert(INSERT, "ue \n")
         text.insert(INSERT, "\nPrincipal Angle 1 = ")
         text.insert(END, math.degrees(ps_angle1))
         text.insert(INSERT, " deg \nPrincipal Angle 2 = ")
         text.insert(END, math.degrees(ps_angle2))
         text.insert(END, " deg")
         text.insert(INSERT, "\nExtreme Shear Angle 1 = ")
         text.insert(END, math.degrees(exshear_angle1))
         text.insert(INSERT, " deg \nExtreme Shear Angle 2 = ")
         text.insert(END, math.degrees(exshear_angle2))
         text.insert(END, " deg")



         text.pack()

         root.mainloop()

         fig,ax = plt.subplots()

         circle=Circle((mohr_centre,0),mohr_radius,edgecolor='blue',facecolor='none')
         ax.add_patch(circle)
         arcp1=Arc((mohr_centre,0),mohr_radius+25,mohr_radius+25,angle=0,theta1=360-2*math.degrees(ps_angle1),theta2=0,color='orange')
         arcp2=Arc((mohr_centre,0),mohr_radius,mohr_radius,angle=0,theta1=360-2*math.degrees(ps_angle1),theta2=360+180,color='purple',lw=2)
         arcex2=Arc((mohr_centre,0),mohr_radius-12,mohr_radius-12,angle=0,theta2=360-2*math.degrees(ps_angle1),theta1=270,color='cyan',lw=2)
         arcex1=Arc((mohr_centre,0),mohr_radius+12,mohr_radius+12,angle=0,theta1=360-2*math.degrees(ps_angle1),theta2=90)
      
         ax.add_patch(arcp1)
         ax.add_patch(arcp2)
         ax.add_patch(arcex2)
         ax.add_patch(arcex1)
         ax.set_aspect('equal','box')
         ax.plot([mohr_centre,principal_strain1,principal_strain2,mohr_centre,mohr_centre,x_normal_strain,y_normal_strain],[0,0,0,shear_strain2,shear_strain1,-shear_strain,shear_strain],'ro')
         ax.text(principal_strain1,0,(principal_strain1,0),ha='left')
         ax.text(principal_strain2,0,(principal_strain2,0),ha='left')
         ax.text(mohr_centre,shear_strain1,(mohr_centre,shear_strain1),ha='right')
         ax.text(mohr_centre,shear_strain2,(mohr_centre,shear_strain2),ha='right')
         ax.text(mohr_centre,0,(mohr_centre,0),ha='right')
         ax.text(x_normal_strain,-shear_strain,(x_normal_strain,shear_strain),ha='left')
         ax.text(y_normal_strain,shear_strain,(y_normal_strain,shear_strain),ha='left')
         ax.text(9.4,-32.7,f'2*theta1={round(2*math.degrees(ps_angle1),3)}')
         ax.text(-322.6,126.9,f'2*theta2={2*math.degrees(ps_angle2)}')
         ax.text(-66.3,144.8,f'2*phi1={2*math.degrees(exshear_angle1)}')
         ax.text(-162.1,-174.3,f'2*phi2={round(2*math.degrees(exshear_angle2),3)}')
         ax.plot([x_normal_strain,y_normal_strain],[-shear_strain,shear_strain],color='green')
         ax.plot([mohr_centre,mohr_centre],[shear_strain2,shear_strain1],color='green')
         ax.plot([principal_strain1,principal_strain2],[0,0],color='black')

         ax.grid(True)


         ax.set_xlim(principal_strain2-1,principal_strain1+1)
         ax.set_ylim(shear_strain2-1,shear_strain1+1)
         ax.set_title('MOHR CIRCLE')
         ax.set_xlabel('Normal Strain(ue)')
         ax.set_ylabel('Shear Strain (ue)')
         plt.show()

class stress:
      def __init__(self):
         
           

         x_normal_stress=float(input("Enter Normal Stress in x-direction  : "))
         y_normal_stress=float(input("Enter Normal Stress in y-direction : "))
         shear_stress=float(input("Enter shear stress on right face : "))

         mohr_centre=(x_normal_stress+y_normal_stress)/2
         mohr_radius=((((x_normal_stress-y_normal_stress)/2)**2)+((shear_stress)**2))**0.5

         ps_angle1=0.5*math.atan((2*shear_stress)/(x_normal_stress-y_normal_stress))
         ps_angle2=ps_angle1+0.5*(math.pi)

         exshear_angle2=0.5*math.atan((x_normal_stress-y_normal_stress)/((-2)*shear_stress))
         exshear_angle1=exshear_angle2+0.5*(math.pi)

         shear_stress1=mohr_radius
         shear_stress2=-mohr_radius

         principal_stress1=((x_normal_stress+y_normal_stress)/2)+mohr_radius
         principal_stress2=((x_normal_stress+y_normal_stress)/2)-mohr_radius

         def onclick():
            pass

         root = Tk()
         text = Text(root)
         text.insert(INSERT, "Maximum Principal Stress = ")
         text.insert(END, principal_stress1)
         text.insert(INSERT, " MPa \nMinimum Principal Stress = ")
         text.insert(END, principal_stress2)
         text.insert(INSERT, " MPa \nMaximum Extreme Shear Stress = ")
         text.insert(END, shear_stress1)
         text.insert(INSERT, " MPa \nMinimum Extreme Shear Stress = ")
         text.insert(END, shear_stress2)
         text.insert(INSERT,"MPa \n")
         text.insert(INSERT, "\nPrincipal Angle 1 = ")
         text.insert(END, math.degrees(ps_angle1))
         text.insert(INSERT, " deg \nPrincipal Angle 2 = ")
         text.insert(END, math.degrees(ps_angle2))
         text.insert(END, " deg")
         text.insert(INSERT, "\nExtreme Shear Angle 1 = ")
         text.insert(END, math.degrees(exshear_angle1))
         text.insert(INSERT, " deg \nExtreme Shear Angle 2 = ")
         text.insert(END, math.degrees(exshear_angle2))
         text.insert(END, " deg")



         text.pack()

         root.mainloop()

         fig1,ax= plt.subplots()

         circless=Circle((mohr_centre,0),mohr_radius,edgecolor='blue',facecolor='none')
         ax.add_patch(circless)
         arcp1=Arc((mohr_centre,0),mohr_radius+25,mohr_radius+25,angle=0,theta1=360-2*math.degrees(ps_angle1),theta2=0,color='orange')
         arcp2=Arc((mohr_centre,0),mohr_radius,mohr_radius,angle=0,theta1=360-2*math.degrees(ps_angle1),theta2=360+180,color='purple',lw=2)
         arcex2=Arc((mohr_centre,0),mohr_radius-12,mohr_radius-12,angle=0,theta2=360-2*math.degrees(ps_angle1),theta1=270,color='cyan',lw=2)
         arcex1=Arc((mohr_centre,0),mohr_radius+12,mohr_radius+12,angle=0,theta1=360-2*math.degrees(ps_angle1),theta2=90)
      
         ax.add_patch(arcp1)
         ax.add_patch(arcp2)
         ax.add_patch(arcex2)
         ax.add_patch(arcex1)
         ax.set_aspect('equal','box')
         ax.plot([mohr_centre,principal_stress1,principal_stress2,mohr_centre,mohr_centre,x_normal_stress,y_normal_stress],[0,0,0,shear_stress2,shear_stress1,-shear_stress,shear_stress],'ro')
         ax.text(principal_stress1,0,(principal_stress1,0),ha='left')
         ax.text(principal_stress2,0,(principal_stress2,0),ha='left')
         ax.text(mohr_centre,shear_stress1,(mohr_centre,shear_stress1),ha='right')
         ax.text(mohr_centre,shear_stress2,(mohr_centre,shear_stress2),ha='right')
         ax.text(mohr_centre,0,(mohr_centre,0),ha='right')
         ax.text(x_normal_stress,-shear_stress,(x_normal_stress,shear_stress),ha='left')
         ax.text(y_normal_stress,shear_stress,(y_normal_stress,shear_stress),ha='left')
         ax.text(-15.7,-5.4,f'2*theta1={2*math.degrees(ps_angle1)}')
         ax.text(-76.7,16.8,f'2*theta2={2*math.degrees(ps_angle2)}',ha='right')
         ax.text(-29.8,26.1,f'2*phi1={2*math.degrees(exshear_angle1)}')
         ax.text(-39,-17.8,f'2*phi2={2*math.degrees(exshear_angle2)}')
         ax.plot([x_normal_stress,y_normal_stress],[-shear_stress,shear_stress],color='green')
         ax.plot([mohr_centre,mohr_centre],[shear_stress2,shear_stress1],color='green')
         ax.plot([principal_stress1,principal_stress2],[0,0],color='black')

         ax.grid(True)


         ax.set_xlim(principal_stress2-1,principal_stress1+1)
         ax.set_ylim(shear_stress2-1,shear_stress1+1)
         ax.set_title('MOHR CIRCLE')
         ax.set_xlabel('Normal Stress (MPA)')
         ax.set_ylabel('Shear Stress (MPA)')
         plt.show()
stress()
strain()