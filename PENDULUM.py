from manim import *
import numpy as np
from scipy.integrate import odeint

g=9.81
def pend(y, t, b, l):
    theta, omega,_ = y
    dy_dt = np.array([ omega, - ( b * omega + g * np.sin(theta) ) / l,0])
    return dy_dt

def path_func(y0,end,B,length):
    sol=odeint(pend,y0,np.linspace(0,end,end*100+1),args=(B,length))
    return lambda t: sol[int(100*t)]
        

class undampenedPendulum(Scene):
    def construct(self):
        length=4

        pend_func=lambda y: pend(y, 0, 0, length)
        pend_field=ArrowVectorField(pend_func, min_color_scheme_value=0, 
                                    max_color_scheme_value=4)
        pend_steam=StreamLines(pend_func,min_color_scheme_value=0, 
                                    max_color_scheme_value=4, stroke_width=3, max_anchors_per_line=30)


        self.add(pend_field)

        self.add(pend_steam)
        pend_steam.start_animation()
        self.wait(10)
        self.play(pend_steam.end_animation())

        self.wait()



class dampenedPendulum(Scene):
    def construct(self):
        length=4
        B=3

        pend_func=lambda y: pend(y, 0, B, length)
        pend_field=ArrowVectorField(pend_func, min_color_scheme_value=0, 
                                    max_color_scheme_value=4)
        pend_steam=StreamLines(pend_func,min_color_scheme_value=0, 
                                    max_color_scheme_value=4, stroke_width=3, max_anchors_per_line=30)


        self.add(pend_field)

        self.add(pend_steam)
        pend_steam.start_animation()
        self.wait(10)
        self.play(pend_steam.end_animation())

        self.wait()

class tranformingPendulum(Scene):
    def construct(self):
        length=4
        B=ValueTracker(0)

        pend_func=lambda y: pend(y, 0, B.get_value(), length)
        
        pend_field=ArrowVectorField(pend_func, min_color_scheme_value=0, 
                                    max_color_scheme_value=4)
        def update_field(mob):
            pend_func=lambda y: pend(y, 0, B.get_value(), length)
            mob.become(ArrowVectorField(pend_func, min_color_scheme_value=0, 
                                    max_color_scheme_value=4))
        pend_field.add_updater(
            lambda mob: update_field(mob)
        )

        blackbox=Rectangle(width=2,height=1,color=BLACK,fill_color=BLACK
                           ).move_to(3*UP).set_z_index(1)
        B_text=Tex("b =",font_size=50).move_to(blackbox.get_center()+0.4*LEFT).set_z_index(2).set_fill(color=BLACK,opacity=1)
        B_val=always_redraw(
            lambda: DecimalNumber(B.get_value(),font_size=50).next_to(B_text,RIGHT,buff=0.1)
            ).set_z_index(2)
        
        self.add(pend_field,B_val,B_text,blackbox)
        self.play(B.animate.set_value(8),run_time=8)
        self.wait()

class Path(Scene):
    def construct(self):
        plane=NumberPlane(background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 4,
                "stroke_opacity": 0.6
            })
        x_label=MathTex(r"\boldsymbol{\theta}")
        y_label=MathTex(r"\boldsymbol{\dot{\theta}}")
        x_label.next_to(plane.get_x_axis().get_right(), UP+LEFT, buff=0.5)
        y_label.next_to(plane.get_y_axis().get_top(), RIGHT+DOWN, buff=0.5)

        self.B=ValueTracker(3)
        self.length=ValueTracker(4)
        self.end=15
        self.pt=[0,0,0]

        black_box=Rectangle(width=2.5,height=1.5).set_fill(color=BLACK,opacity=1).move_to(5.5*LEFT+2*UP)
        self.B_text=always_redraw(lambda:
                                  DecimalNumber(self.B.get_value()).next_to(black_box.get_top(),
                                                              DOWN+0.5*RIGHT
                                                              ))
        self.L_text=always_redraw(lambda: 
                                  DecimalNumber(
            self.length.get_value()).next_to(self.B_text,DOWN
                                             ))


        B_tex=MathTex(r"b =",font_size=50).next_to(self.B_text,LEFT,buff=0.2)
        L_tex=MathTex(r"l =",font_size=50).next_to(self.L_text,LEFT,buff=0.2)
        self.path_start=Dot(self.pt)
        path_curve=path_func([0,0,0],self.end,self.B.get_value(),self.length.get_value())
        self.path=ParametricFunction(path_curve,t_range=np.array([0,self.end]),stroke_width=5)


        self.add(plane,x_label,y_label,self.path_start,self.path,black_box,
                 self.B_text,self.L_text,B_tex,L_tex)
        self.interactive_embed()


    def on_key_press(self, symbol, modifiers):
        def animateS():
            path_curve=path_func(self.pt,self.end,self.B.get_value(),self.length.get_value())

            self.play(self.path_start.animate.move_to(self.pt),FadeOut(self.path))
            
            self.path=ParametricFunction(path_curve,t_range=np.array([0,self.end]),stroke_width=5)

            self.play(Create(self.path),rate_func=rush_into)
        from pyglet.window import key as pyglet_key
        if symbol==pyglet_key.B:
            self.play(self.B.animate.set_value(self.B.get_value()-0.5))
        if symbol==pyglet_key.P:
            self.pt=self.mouse_point.get_center()
            animateS()
        if symbol==pyglet_key.N:
            self.play(self.B.animate.set_value(self.B.get_value()+0.5))
        if symbol==pyglet_key.L:
            self.play(self.length.animate.set_value(self.length.get_value()+0.5))
        if symbol==pyglet_key.O:
            self.play(self.length.animate.set_value(self.length.get_value()-0.5))
        super().on_key_press(symbol,modifiers)
        

class TransformPath(Scene):
    def construct(self):
        plane=NumberPlane(background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 4,
                "stroke_opacity": 0.6
            })

        x_label=MathTex(r"\boldsymbol{\theta}")
        y_label=MathTex(r"\boldsymbol{\dot{\theta}}")
        x_label.next_to(plane.get_x_axis().get_right(), UP+LEFT, buff=0.5)
        y_label.next_to(plane.get_y_axis().get_top(), RIGHT+DOWN, buff=0.5)

        y0=[0,1,0]
        B=ValueTracker(0)
        b_final=8
        length=4
        end=12
        t=np.linspace(0,end,end*10+1)
        
        sol=odeint(pend,y0,t,args=(B.get_value(),length))
        path_func=lambda t: sol[int(10*t)]
        

        path=ParametricFunction(path_func,t_range=np.array([0,end]),stroke_width=5)

        def updatePath(mob):
            sol=odeint(pend,y0,np.linspace(0,end,end*10+1),args=(B.get_value(),length))
            path_func=lambda t: sol[int(10*t)]
            mob.become(ParametricFunction(path_func,t_range=np.array([0,end]),stroke_width=5))
        path.add_updater(
            lambda mob: updatePath(mob)
        )
        blackbox=Rectangle(width=2,height=1,color=BLACK
                           ).move_to(2*UP).set_z_index(1).set_fill(color=BLACK,opacity=1)
        B_text=Tex("b =",font_size=50).move_to(blackbox.get_center()+LEFT*0.4).set_z_index(2)
        B_val=always_redraw(
            lambda: DecimalNumber(B.get_value(),font_size=50).next_to(B_text,RIGHT,buff=0.1)
            ).set_z_index(2)


        self.add(plane,path,x_label,y_label,B_val,B_text,blackbox)
        self.play(B.animate.set_value(b_final),run_time=8)
        self.wait()


class TransformGraph(Scene):
    def construct(self):

        y0=[0,1,0]
        b=3
        length=ValueTracker(4)
        l_final=8
        end=12
        t=np.linspace(0,end,end*10+1)
        
        sol=odeint(pend,y0,t,args=(b,length.get_value()))
        path_func=lambda t: sol[int(10*t)]
        theta_func=lambda t: path_func(t)[0]
        omega_func=lambda t: path_func(t)[1]
        
        pend_ax=Axes(x_range=[0,end],y_range=[-1,1,.5],
                   tips=False,axis_config={"include_numbers": True}
                   ).shift(0.1*(5*RIGHT))
        theta_curve=pend_ax.plot(theta_func,color=RED)
        omega_curve=pend_ax.plot(omega_func,color=BLUE)


        label_1 = pend_ax.get_graph_label(theta_curve, 
                                          MathTex(r"\boldsymbol{\theta}"), x_val=1, direction=UP
                                          ).shift(0.75*UP)
        
        label_2 =pend_ax.get_graph_label(omega_curve, 
                                         MathTex(r"\boldsymbol{\dot{\theta}}"), x_val=1.5, direction=DOWN)
        
        x_label = pend_ax.get_x_axis_label(
            Tex("Time (seconds)").scale(0.65), edge=DOWN, direction=DOWN
        ).shift(DOWN)
        y_label = pend_ax.get_y_axis_label(
            Tex("Theta-Omega (radians)").scale(0.65).rotate(90 * DEGREES),
            edge=LEFT,
            direction=LEFT
        )
        title = Title(
            "Pendulum Over Time  ",include_underline=False
        )
        def updateTheta(mob):
            sol=odeint(pend,y0,t,args=(b,length.get_value()))
            path_func=lambda t: sol[int(10*t)]
            theta_func=lambda t: path_func(t)[0]
            mob.become(pend_ax.plot(theta_func,color=RED))
        def updateOmega(mob):
            sol=odeint(pend,y0,t,args=(b,length.get_value()))
            path_func=lambda t: sol[int(10*t)]
            omega_func=lambda t: path_func(t)[1]
            mob.become(pend_ax.plot(omega_func,color=BLUE))

        theta_curve.add_updater(
            lambda mob: updateTheta(mob)
        )
        omega_curve.add_updater(
            lambda mob: updateOmega(mob)
        )

        l_text=Tex("l =",font_size=50,color=YELLOW).move_to(3.5*RIGHT+1.75*UP)
        l_val=always_redraw(
            lambda: DecimalNumber(length.get_value(),font_size=50,color=YELLOW).next_to(l_text,RIGHT,buff=0.1)
            )


        self.play(*[Write(mob) for mob in [pend_ax,title,x_label,y_label]])
        self.wait()
        self.play(*[Write(mob) for mob in [theta_curve,omega_curve,label_1,label_2,l_val,l_text]],run_time=8)
        self.wait()
        self.play(length.animate.set_value(l_final),run_time=8)
        self.wait()


