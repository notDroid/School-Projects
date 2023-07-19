from manim import *
import numpy as np
from scipy.integrate import odeint

g=9.81
def diff(y, t, r_gr, r_dp,f_gp,f_dr):
    rabbit, fox,_= y
    dy_dt = np.array([ r_gr*rabbit-r_dp*rabbit*fox, f_gp*rabbit*fox-f_dr*fox,0])
    return dy_dt
def diff_fix(y, t, r_gr, r_dp,f_gp,f_dr):
    rabbit, fox= y
    dy_dt = np.array([ r_gr*rabbit-r_dp*rabbit*fox, f_gp*rabbit*fox-f_dr*fox])
    return dy_dt

def path_func(y0,end,r_gr, r_dp,f_gp,f_dr):
    sol=odeint(diff,y0,np.linspace(0,end,end*100+1),args=(r_gr, r_dp,f_gp,f_dr))-np.array([7.11, 4, 0])
    return lambda t: sol[int(100*t)]
def path_func_fix(y0,end,r_gr, r_dp,f_gp,f_dr):
    sol=odeint(diff_fix,y0,np.linspace(0,end,end*10+1),args=(r_gr, r_dp,f_gp,f_dr))
    return lambda t: sol[int(10*t)]     

class sloppyField(Scene):
    def construct(self):
        r_gr, r_dp,f_gp,f_dr=2,1,1,2
        top_right_corner = [self.camera.frame_width / 2, self.camera.frame_height / 2, 0]

        pp_func=lambda y: diff(y+top_right_corner, 0, r_gr, r_dp,f_gp,f_dr)
        pp_field=ArrowVectorField(pp_func,min_color_scheme_value=0, 
                                    max_color_scheme_value=30)
        pp_steam=StreamLines(pp_func, min_color_scheme_value=0, 
                                    max_color_scheme_value=30, stroke_width=3, max_anchors_per_line=30)

        self.add(pp_field)

        self.add(pp_steam)
        pp_steam.start_animation()
        self.wait(10)
        self.play(pp_steam.end_animation())
        self.wait()

class Path(Scene):
    def construct(self):
        #7.11,4
        bottom_left_corner = np.array([-7.11, -4, 0])
        self.top_right_corner = np.array([7.11, 4, 0])
        plane=NumberPlane(background_line_style={
                "stroke_color": TEAL,
                "stroke_width": 4,
                "stroke_opacity": 0.6
            }).scale(2).move_to(bottom_left_corner)
        x_label=MathTex(r"\boldsymbol{x}")
        y_label=MathTex(r"\boldsymbol{y}")
        x_label.next_to(plane.get_x_axis().get_right(), UP+LEFT, buff=0.5)
        y_label.next_to(plane.get_y_axis().get_top(), RIGHT+DOWN, buff=0.5)

        self.r_gr, self.r_dp,self.f_gp,self.f_dr=[ValueTracker(i) for i in [2,1,1,2]]
        self.end=15
        self.pt=bottom_left_corner

        black_box=Rectangle(width=7,height=2.5).set_fill(color=BLACK,opacity=1).move_to(3*RIGHT+2*UP)
        self.r_gr_text=always_redraw(lambda:
                                  DecimalNumber(self.r_gr.get_value()).next_to(black_box.get_top(),
                                                              DOWN+9*RIGHT
                                                              ))
        self.r_dp_text=always_redraw(lambda: 
                                  DecimalNumber(
            self.r_dp.get_value()).next_to(self.r_gr_text,DOWN
                                             ))
        self.f_gp_text=always_redraw(lambda: 
                                  DecimalNumber(
            self.f_gp.get_value()).next_to(self.r_dp_text,DOWN
                                             ))
        self.f_dr_text=always_redraw(lambda: 
                                  DecimalNumber(
            self.f_dr.get_value()).next_to(self.f_gp_text,DOWN
                                             ))

        r_gp_tex=Tex(r"Prey Growth Rate =",font_size=50).next_to(self.r_gr_text,LEFT,buff=0.2)
        r_dp_tex=Tex(r"Preditation Rate =",font_size=50).next_to(self.r_dp_text,LEFT,buff=0.2)
        f_gp_tex=Tex(r"Preditation Growth =",font_size=50).next_to(self.f_gp_text,LEFT,buff=0.2)
        f_dr_tex=Tex(r"Predator Death Rate =",font_size=50).next_to(self.f_dr_text,LEFT,buff=0.2)
        self.path_start=Dot(self.pt)
        
        path_curve=path_func(self.pt+self.top_right_corner,self.end,self.r_gr.get_value(), self.r_dp.get_value(),
                             self.f_gp.get_value(),self.f_dr.get_value())
        self.path=ParametricFunction(path_curve,t_range=np.array([0,self.end]),stroke_width=5)


        self.add(plane,x_label,y_label,self.path_start,self.path,black_box,
                 self.r_dp_text,self.f_gp_text,self.r_gr_text,self.f_dr_text,
                 r_gp_tex,r_dp_tex,f_gp_tex,f_dr_tex)
        self.interactive_embed()


    def on_key_press(self, symbol, modifiers):
        def animateS():
            path_curve=path_func(self.pt+self.top_right_corner,self.end,self.r_gr.get_value(), self.r_dp.get_value(),
                                 self.f_gp.get_value(),self.f_dr.get_value())

            self.play(self.path_start.animate.move_to(self.pt),FadeOut(self.path))
            
            self.path=ParametricFunction(path_curve,t_range=np.array([0,self.end]),stroke_width=5)

            self.play(Create(self.path),rate_func=rush_into,run_time=3)
        from pyglet.window import key as pyglet_key
        if symbol==pyglet_key.P:
            self.pt=self.mouse_point.get_center()
            animateS()
        if symbol==pyglet_key.E:
            self.play(self.r_gr.animate.set_value(self.r_gr.get_value()-0.5))
        if symbol==pyglet_key.R:
            self.play(self.r_gr.animate.set_value(self.r_gr.get_value()+0.5))
        if symbol==pyglet_key.D:
            self.play(self.r_dp.animate.set_value(self.r_dp.get_value()-0.5))
        if symbol==pyglet_key.F:
            self.play(self.r_dp.animate.set_value(self.r_dp.get_value()+0.5))
        if symbol==pyglet_key.X:
            self.play(self.f_gp.animate.set_value(self.f_gp.get_value()-0.5))
        if symbol==pyglet_key.C:
            self.play(self.f_gp.animate.set_value(self.f_gp.get_value()+0.5))
        if symbol==pyglet_key.T:
            self.play(self.f_dr.animate.set_value(self.f_dr.get_value()-0.5))
        if symbol==pyglet_key.Y:
            self.play(self.f_dr.animate.set_value(self.f_dr.get_value()+0.5))
        super().on_key_press(symbol,modifiers)
      
class ppGraph(Scene):
    def construct(self):
        y0,end,r_gr, r_dp,f_gp,f_dr=[10,10],10,2,1,1,2
        pp_func=path_func_fix(y0,end,r_gr, r_dp,f_gp,f_dr)
        pp_func_prey=lambda x: pp_func(x)[0]
        pp_func_predator=lambda x: pp_func(x)[1]

        pp_ax=Axes(x_range=[0,10],y_range=[0,18,2],
                   tips=False,axis_config={"include_numbers": True}
                   ).shift(0.1*(2*UP+RIGHT))
        pp_curve_prey=pp_ax.plot(pp_func_prey,color=BLUE)
        pp_curve_predator=pp_ax.plot(pp_func_predator,color=RED)


        label_1 = pp_ax.get_graph_label(pp_curve_prey, "Prey", x_val=5.5, direction=LEFT)
        label_2 =pp_ax.get_graph_label(pp_curve_predator, "Predator", x_val=6.5, direction=RIGHT)
        labels = VGroup(label_1, label_2)

        x_label = pp_ax.get_x_axis_label(
            Tex("Time (years)").scale(0.65), edge=DOWN, direction=DOWN
        )
        y_label = pp_ax.get_y_axis_label(
            Tex("Prey-Predator Number").scale(0.65).rotate(90 * DEGREES),
            edge=LEFT,
            direction=LEFT
        )
        title = Title(
            " Population of Predator VS Prey over Time ",include_underline=False
        )

        self.play(*[Write(mob) for mob in [pp_ax,x_label,y_label,title]])
        self.wait()
        self.play(Write(labels),
                  Write(pp_curve_prey,run_time=7),
                  Write(pp_curve_predator,run_time=7))
        self.wait(5)

class pp(Scene):
    def construct(self):
        prey=Tex("Prey =").move_to(LEFT)
        predator=Tex("Predator =").next_to(prey,3*DOWN)
        x=MathTex("x").next_to(prey,RIGHT)
        y=MathTex("y").next_to(predator,RIGHT)
        pandp=VGroup(prey,predator,x,y)

        prey_r=Tex("Rate of Change of Prey =",font_size=70).move_to(2.5*UP).shift(LEFT)
        predator_r=Tex("Rate of Change of Predator =",font_size=70).move_to(2.5*UP).shift(LEFT)
        dx_dt=MathTex(r"\frac{dx}{dt} =",font_size=60).next_to(prey_r,2.5*DOWN).shift(LEFT)
        dy_dt=MathTex(r"\frac{dy}{dt} =",font_size=60).next_to(predator_r,2.5*DOWN).shift(LEFT)

        prey_in=Tex("Prey In",font_size=60).next_to(dx_dt,RIGHT)
        dx_dt_in=MathTex(r"\alpha x",font_size=60).next_to(dx_dt,RIGHT)
        alpha=MathTex(r"\alpha = Prey Growth Rate",font_size=50).move_to(1.5*DOWN+LEFT)

        prey_out=Tex("- Prey Out",font_size=60).next_to(prey_in,RIGHT)
        dx_dt_out=MathTex(r"- \beta x y",font_size=60).next_to(dx_dt_in,RIGHT)
        beta=MathTex(r"\beta = Predatation Rate",font_size=50).next_to(alpha,DOWN)

        predator_in=Tex("Predator In",font_size=60).next_to(dy_dt,RIGHT)
        dy_dt_in=MathTex(r"\gamma x y",font_size=60).next_to(dy_dt,RIGHT)
        gamma=MathTex(r"\gamma = Predatation Growth Rate",font_size=50).move_to(1.5*DOWN+LEFT)

        predator_out=Tex("- Predator Out",font_size=60).next_to(predator_in,RIGHT)
        dy_dt_out=MathTex(r"- \delta y",font_size=60).next_to(dy_dt_in,RIGHT)
        delta=MathTex(r"\delta = Predator Death Rate",font_size=50).next_to(gamma,DOWN)

        dy_dt_f=VGroup(dy_dt,dy_dt_in,dy_dt_out)
        dx_dt_f=VGroup(dx_dt,dx_dt_in,dx_dt_out)

        eq=Title("Lotka–Volterra Equations",font_size=90).move_to(2*UP)
        self.play(Write(eq))
        self.wait()
        self.play(Write(prey),Write(predator))
        self.wait()
        self.play(AnimationGroup(Write(x),Write(y),lag_ratio=0.5))
        self.wait()
        self.play(Unwrite(pandp),Unwrite(eq))
        self.play(Write(prey_r))
        self.wait()
        self.play(Write(dx_dt))
        self.wait()
        self.play(Write(prey_in),Write(prey_out))
        self.wait()
        self.play(ReplacementTransform(prey_in,dx_dt_in))
        self.play(Write(alpha))
        self.wait()
        self.play(ReplacementTransform(prey_out,dx_dt_out))
        self.play(Write(beta))
        self.wait()
        self.play(*[Unwrite(mob) for mob in [prey_r,
                                             dx_dt,dx_dt_in,dx_dt_out,alpha,beta]])
        self.play(Write(predator_r))
        self.wait()
        self.play(Write(dy_dt))
        self.wait()
        self.play(Write(predator_in),Write(predator_out))
        self.wait()
        self.play(ReplacementTransform(predator_in,dy_dt_in))
        self.play(Write(gamma))
        self.wait()
        self.play(ReplacementTransform(predator_out,dy_dt_out))
        self.play(Write(delta))
        self.wait()
        self.play(*[Unwrite(mob) for mob in [predator_r,
                                             dy_dt,dy_dt_in,dy_dt_out,gamma,delta]])
        
        dy_dt.shift(3*DOWN)
        dy_dt_in.shift(3*DOWN)
        dy_dt_out.shift(3*DOWN)
        self.play(*[Create(mob) for mob in [dy_dt,dy_dt_in,dy_dt_out,dx_dt,dx_dt_in,dx_dt_out]])
        self.wait(2)
        

