from manim import *
import numpy as np
class Derivatives(Scene):
    def construct(self):
        ax=Axes(x_range=[0,5,1],y_range=[0,100,10],tips=False)
        func=ax.plot(lambda x:np.exp(x)+9,x_range=[0,5],color=BLUE)
        self.play(Create(ax),Create(func))
        self.wait()

        c=ValueTracker(2.5)

        moving_tangent=always_redraw(lambda: ax.get_secant_slope_group(
            x=c.get_value(),
            graph=func,
            dx=0.01,
            secant_line_length=10,
            secant_line_color=GREEN
            )
        )

        moving_point=always_redraw(lambda: Dot(ax.c2p(c.get_value(),np.exp(c.get_value())+9)).scale(0.75))

        self.play(Create(moving_tangent),Create(moving_point))
        self.play(c.animate.set_value(2.6),rate_func=wiggle,run_time=2)
        self.wait()
        self.play(FadeOut(ax),FadeOut(moving_tangent),FadeOut(func),FadeOut(moving_point))

        f_axis=NumberLine(x_range=[0,1,0.1],length=10,include_numbers=True).scale(1.15).shift(UP)
        x_axis=NumberLine(x_range=[0,1,0.1],length=10,include_numbers=True).scale(1.15).next_to(f_axis,DOWN,buff=1)
        
        f_text=always_redraw(lambda:MathTex("f").next_to(f_axis,LEFT,buff=0.2).shift(UP*0.05))
        x_text=always_redraw(lambda:MathTex("x").next_to(x_axis,LEFT,buff=0.2).shift(UP*0.05))

        f_pt1=Dot(f_axis.n2p(0.4))
        x_pt1=Dot(x_axis.n2p(0.2))

        dx=ValueTracker(0)
        f_pt2=always_redraw(lambda:Dot(f_axis.n2p(0.4+2*dx.get_value())))
        x_pt2=always_redraw(lambda:Dot(x_axis.n2p(0.2+dx.get_value())))

        f_line=always_redraw(lambda:Line(f_axis.n2p(0.4),f_axis.n2p(0.4+2*dx.get_value()),color=BLUE))
        x_line=always_redraw(lambda:Line(x_axis.n2p(0.2),x_axis.n2p(0.2+dx.get_value()),color=YELLOW))

        dx_text=always_redraw(lambda:MathTex("dx",color=YELLOW).next_to(x_line,UP))
        df_text=always_redraw(lambda:MathTex("df",color=BLUE).next_to(f_line,UP))

        self.play(Create(f_axis),Create(x_axis))
        self.play(Create(f_text),Create(x_text))
        self.wait()
        self.play(Create(f_pt1),Create(x_pt1),Create(f_pt2),Create(x_pt2),Create(f_line),Create(x_line))
        self.wait()
        self.play(Write(dx_text),Write(df_text))
        self.play(dx.animate.set_value(0.1),runtime=15)
        self.play(FadeOut(f_pt2),FadeOut(x_pt2),FadeOut(f_pt1),FadeOut(x_pt1))
        self.wait()

        eq_dx=MathTex("dx",color=YELLOW,font_size=70).shift(3*LEFT+2*UP)
        eq_scalefactor=Text("scale factor",gradient=(YELLOW,BLUE),slant=ITALIC,font_size=45).next_to(eq_dx,RIGHT).shift(DOWN*0.05)
        eq_df=MathTex("= df",color=BLUE,font_size=70).next_to(eq_scalefactor,RIGHT)
        
        self.play(x_axis.animate.shift(2*DOWN),f_axis.animate.shift(2*DOWN))
        self.wait()
        self.play(Write(eq_dx))
        self.play(Write(eq_scalefactor))
        self.play(Write(eq_df))
        
        dxtodf1=x_line.copy()
        dxtodf2=f_line.copy()
        eq_df_dx=MathTex(r"\frac{df}{dx}",color=GREEN,font_size=70).next_to(eq_dx,RIGHT)
        text_2=MathTex("2",font_size=70,color=GREEN).next_to(eq_df_dx,LEFT)
        dx_right=eq_dx.copy().next_to(text_2,RIGHT)

        self.wait()
        self.add(dxtodf1)
        self.play(ReplacementTransform(dxtodf1,dxtodf2))
        self.wait()
        self.play(ReplacementTransform(eq_scalefactor,eq_df_dx),eq_df.animate.next_to(eq_dx,RIGHT,buff=1.25))
        self.wait()
        self.play(ReplacementTransform(eq_dx,text_2),ReplacementTransform(eq_df_dx,dx_right))

        self.wait()
        dxtodf1=x_line.copy()
        dxtodf2=f_line.copy()
        self.add(dxtodf1)
        self.play(ReplacementTransform(dxtodf1,dxtodf2))        
        self.wait()

def ccbox(string="",color=WHITE):
    result = VGroup() # create a VGroup
    box = Rectangle(  # create a box
        height=2, width=3, fill_color=color, 
        fill_opacity=0.15
    ).scale(0.75)
    text = MathTex(string,font_size=50).move_to(box.get_center()) # create text
    result.add(box, text) # add both objects to the VGroup
    return result
def ccline(box1,box2):
    return Line(box1.get_center()+.75*1.5*RIGHT,box2.get_center()+.75*1.5*LEFT)


class ChainRule(MovingCameraScene):
    def construct(self):
        func=MathTex(r"f(x) = \sigma(x^2)",font_size=70)

        self.add(func)
        self.wait(2)
        self.play(func.animate.move_to(2.5*UP))
        

        x_box=ccbox(r"x",RED).move_to(4*LEFT+DOWN)
        z_box=ccbox(r"z = x^2",PURPLE).next_to(x_box,4*RIGHT)
        f_box=ccbox(r"f = \sigma(z)",YELLOW).next_to(z_box,4*RIGHT)
        xtoz=ccline(x_box,z_box)
        ztof=ccline(z_box,f_box)

        self.play(Create(x_box))
        self.wait()
        self.play(Create(z_box),Create(xtoz))
        self.wait()
        self.play(Create(f_box),Create(ztof))
        self.wait()

        def caxis(box,label):
            result=VGroup()
            nline=NumberLine(x_range=[0,1,0.2],length=1).scale(.6*box.get_width()).next_to(box,1.5*DOWN)
            text=MathTex(label,font_size=30).next_to(nline,LEFT)
            result.add(nline,text)
            return result
        
        x_axis=caxis(x_box,"x")
        x_dot=Dot(x_axis[0].n2p(0.2),color=RED).scale(0.75)
        x_dot2=x_dot.copy()
        dx_line=Line(x_axis[0].n2p(0.2),x_axis[0].n2p(0.2),color=RED)

        z_axis=caxis(z_box,"z")
        z_dot=Dot(z_axis[0].n2p(0.4),color=PURPLE).scale(0.75)
        z_dot2=z_dot.copy()
        dz_line=Line(z_axis[0].n2p(0.4),z_axis[0].n2p(0.4),color=PURPLE)

        f_axis=caxis(f_box,"f")
        f_dot=Dot(f_axis[0].n2p(0.8),color=YELLOW).scale(0.75)
        f_dot2=f_dot.copy()
        df_line=Line(f_axis[0].n2p(0.8),f_axis[0].n2p(0.8),color=YELLOW)

        self.play(self.camera.frame.animate.move_to(x_box).scale(0.5),Write(x_axis))
        self.play(Create(x_dot),Create(x_dot2))
        self.play(x_dot2.animate.move_to(x_axis[0].n2p(0.4)),dx_line.animate.put_start_and_end_on(x_axis[0].n2p(0.2),x_axis[0].n2p(0.4)))
        self.wait()

        self.play(self.camera.frame.animate.move_to(z_box),Write(z_axis))
        self.play(Create(z_dot),Create(z_dot2))
        self.play(z_dot2.animate.move_to(z_axis[0].n2p(0.8)),dz_line.animate.put_start_and_end_on(z_axis[0].n2p(0.4),z_axis[0].n2p(0.8)))
        self.wait()

        self.play(self.camera.frame.animate.move_to(f_box),Write(f_axis))
        self.play(Create(f_dot),Create(f_dot2))
        self.play(f_dot2.animate.move_to(f_axis[0].n2p(0.7)),df_line.animate.put_start_and_end_on(f_axis[0].n2p(0.7),f_axis[0].n2p(0.8)))
        self.wait()
        self.remove(func,sigmoid)

        self.play(self.camera.frame.animate.move_to(z_box.get_center()+2*DOWN).scale(2))
        self.wait()

        df_text=MathTex("df",font_size=70,color=YELLOW).move_to(4.5*DOWN+3*LEFT)
        etext=MathTex("=",font_size=70).next_to(df_text,RIGHT)
        df_dz_text=MathTex(r"\frac{df}{dz}",font_size=70).next_to(etext,RIGHT)
        dz_text=MathTex("dz",font_size=70,color=PURPLE).next_to(df_dz_text,RIGHT)
        dz_dx_text=MathTex(r"\frac{dz}{dx}",font_size=70).next_to(df_dz_text,RIGHT)
        dx_text=MathTex("dx",font_size=70,color=RED).next_to(dz_dx_text,RIGHT)

        self.play(Write(df_text),Write(etext))
        self.play(Write(df_dz_text),Write(dz_text))
        self.play(AnimationGroup(ReplacementTransform(dz_text,dz_dx_text),Write(dx_text),lag_ratio=0.5))
        self.wait(2)

def cbox(col,string,size=40):
    result=VGroup()
    box=Rectangle(height=1,width=3).set_fill(color=col,opacity=0.2).scale(0.75)
    text=MathTex(string,font_size=size).move_to(box.get_center())
    result.add(box,text)
    return result
def cline(box1,box2):
    return Line(box1.get_center()+RIGHT*box1.get_width()/2,box2.get_center()+LEFT*box2.get_width()/2)

class backprop(MovingCameraScene):
    def construct(self):
        x1_box=cbox(RED,r"x_{1}").move_to(5.8*LEFT+UP*0.5)
        x2_box=cbox(RED,r"x_{2}").next_to(x1_box,3*DOWN)
    
        w1_middle_box=cbox(BLUE,r"w_{1}").next_to(x1_box,1.5*UP).shift(RIGHT*0.2)
        w2_middle_box=cbox(BLUE,r"w_{2}").next_to(x2_box,1.5*DOWN).shift(RIGHT*0.2)
        
        z_middle_box=cbox(PURPLE,r"z=w_{1}x_{1}+w_{2}x_{2}+b",20).next_to(x1_box,DOWN+2.5*RIGHT)
        
        b_middle_box=cbox(PINK,r"b").next_to(z_middle_box,2*UP)
        
        a_middle_box=cbox(WHITE,r"a=\sigma(z)").next_to(z_middle_box,2.5*RIGHT)
        
        w_end=cbox(BLUE,r"w").next_to(a_middle_box,1.5*UP).shift(RIGHT*0.2)
        
        z_end=cbox(PURPLE,r"z=wa+b").next_to(a_middle_box,2.5*RIGHT)
        
        b_end=cbox(PINK,r"b").next_to(z_end,2*UP)
        
        a_end=cbox(WHITE,r"a=\sigma(z)").next_to(z_end,2.5*RIGHT)
        
        x1z=cline(x1_box,z_middle_box)
        x2z=cline(x2_box,z_middle_box)
        
        w1z=cline(w1_middle_box,z_middle_box)
        w2z=cline(w2_middle_box,z_middle_box)
        
        b1z=Line(b_middle_box.get_center()+DOWN*b_middle_box.get_height()/2,z_middle_box.get_center()+UP*z_middle_box.get_height()/2)
        
        z1a=cline(z_middle_box,a_middle_box)
        
        az=cline(a_middle_box,z_end)
        
        wz=cline(w_end,z_end)
        
        bz=Line(b_end.get_center()+DOWN*b_end.get_height()/2,z_end.get_center()+UP*z_end.get_height()/2)
        
        za=cline(z_end,a_end)
        
        cgraph=VGroup(x1_box,x2_box,w1_middle_box,w2_middle_box,b_middle_box,z_middle_box,a_middle_box,w_end,b_end,z_end,a_end,x1z,x2z,w1z,w2z,b1z,z1a,az,wz,bz,za)
        
        self.play(Create(x1_box),Create(x2_box))
        self.play(Create(z_middle_box),Create(x1z),Create(x2z))
        self.play(AnimationGroup(Create(w1_middle_box),Create(w2_middle_box),Create(b_middle_box),Create(w1z),Create(w2z),Create(b1z),lag_ratio=1))
        self.play(Create(a_middle_box),Create(z1a))
        self.play(Create(z_end),Create(az))
        self.play(AnimationGroup(Create(w_end),Create(b_end),Create(wz),Create(bz),lag_ratio=1))
        self.play(Create(a_end),Create(za))
        self.wait()
        
        self.camera.frame.save_state()
        cgraph.save_state()

        dw_end=MathTex("dw",font_size=40).move_to(w_end)
        dz_end=MathTex("dz",font_size=40).move_to(z_end)
        da_end=MathTex("da",font_size=40).move_to(a_end)
        
        self.play(AnimationGroup(self.camera.frame.animate.move_to(w_end).scale(0.5),ReplacementTransform(w_end[1],dw_end),lag_ratio=0.5))
        self.play(AnimationGroup(self.camera.frame.animate.move_to(z_end),ReplacementTransform(z_end[1],dz_end),lag_ratio=0.5))
        self.play(AnimationGroup(self.camera.frame.animate.move_to(a_end),ReplacementTransform(a_end[1],da_end),lag_ratio=0.5))

        self.play(*[FadeOut(mob) for mob in (cgraph[:7]+cgraph[11:16]+cgraph[8]+cgraph[-2]+cgraph[-4]+cgraph[-5])])
        self.play(self.camera.frame.animate.move_to(z_end.get_center()+DOWN).scale(1.5))
        self.wait()
        
        df=MathTex("df =",font_size=70).next_to(z_end,5*DOWN+1.5*LEFT)
        df_dz=MathTex(r"\frac{df}{dz}",font_size=70).next_to(df,RIGHT)
        dz=MathTex("dz",font_size=70).next_to(df_dz,RIGHT)
        dz_dw=MathTex(r"\frac{dz}{dw}",font_size=70).next_to(df_dz,RIGHT)
        dw=MathTex("dw",font_size=70).next_to(dz_dw,RIGHT)
        
        self.play(AnimationGroup(Write(df),Write(df_dz),Write(dz),lag_ratio=1))
        self.play(AnimationGroup(ReplacementTransform(dz,dz_dw),Write(dw),lag_ratio=0.5))
        self.wait()
        self.play(AnimationGroup(FadeOut(df),FadeOut(df_dz),FadeOut(dz_dw),FadeOut(dw),lag_ratio=0.25))
        self.play(self.camera.frame.animate.restore(),cgraph.animate.restore(),*[FadeOut(mob) for mob in [dw_end,dz_end,da_end]])
        self.wait()

        dw_middle=MathTex("dw",font_size=40).move_to(w1_middle_box)
        dz_middle=MathTex("dz",font_size=40).move_to(z_middle_box)
        da_middle=MathTex("da",font_size=40).move_to(a_middle_box)
                  
        self.play(*[FadeOut(mob) for mob in cgraph[:2]+cgraph[3:5]+cgraph[7:9]+cgraph[11:13]+cgraph[14:16]+cgraph[18:20]])
        self.play(self.camera.frame.animate.shift(DOWN))
        self.play(ReplacementTransform(w1_middle_box[1],dw_middle))
        self.play(ReplacementTransform(z_middle_box[1],dz_middle))
        self.play(ReplacementTransform(a_middle_box[1],da_middle))
        self.play(ReplacementTransform(z_end[1],dz_end))
        self.play(ReplacementTransform(a_end[1],da_end))
        self.wait()

        df=df.move_to(self.camera.frame.get_center()+2*DOWN+5*LEFT)
        df_dz=MathTex(r"\frac{df}{dz}",font_size=70).next_to(df,RIGHT)
        dz=MathTex("dz",font_size=70).next_to(df_dz,RIGHT)
        dz_da=MathTex(r"\frac{dz}{da}",font_size=70).next_to(df_dz,RIGHT)
        da=MathTex("da",font_size=70).next_to(dz_da,RIGHT)
        da_dz_middle=MathTex(r"\frac{da}{dz_{middle}}",font_size=70).next_to(dz_da,RIGHT)
        dz_middle=MathTex("dz_{middle}",font_size=70).next_to(da_dz_middle,RIGHT)
        dz_dw_middle=MathTex(r"\frac{dz_{middle}}{dw_{middle}}",font_size=70).next_to(da_dz_middle,RIGHT)
        dw_middle=MathTex(r"dw_{middle}",font_size=70).next_to(dz_dw_middle,RIGHT)

        self.play(AnimationGroup(Write(df),Write(df_dz),Write(dz),lag_ratio=1))
        self.play(AnimationGroup(ReplacementTransform(dz,dz_da),Write(da),lag_ratio=1))
        self.play(AnimationGroup(ReplacementTransform(da,da_dz_middle),Write(dz_middle),lag_ratio=1))
        self.play(AnimationGroup(ReplacementTransform(dz_middle,dz_dw_middle),Write(dw_middle),lag_ratio=1))
        self.wait()


class intro(Scene):
    def construct(self):
        input_text=Tex("input",font_size=70).move_to(5.5*LEFT)
        nn_box=Square(side_length=4).move_to(0.5*LEFT)
        nn_box_text=Tex(r"Nueral \\Network",font_size=70).move_to(nn_box.get_center())
        nn=VGroup(nn_box,nn_box_text)
        output_text=Tex("prediction",font_size=70).move_to(5*RIGHT)

        tonn=Arrow(input_text.get_center()+RIGHT,nn_box.get_center()+2*LEFT)
        fromnn=Arrow(nn_box.get_center()+2*RIGHT,output_text.get_center()+1.5*LEFT)

        self.play(AnimationGroup(Write(input_text),Write(tonn),Write(nn),Write(fromnn),Write(output_text),lag_ratio=1))
        self.wait()

        cancer_text=Tex("cancer",font_size=70).move_to(output_text)
        inputs_text=Tex(r"tumor size \\ max length", font_size=45).move_to(input_text)

        self.play(ReplacementTransform(output_text,cancer_text))
        self.wait()
        self.play(ReplacementTransform(input_text,inputs_text))
        self.wait()

        cancer_prob_text=Tex(r"cancer \\ probability",font_size=55).move_to(cancer_text)

        self.play(ReplacementTransform(cancer_text,cancer_prob_text))
        self.wait()

class NN(MovingCameraScene):
    def construct(self):
        def node():return Circle(radius=0.25,color=WHITE,stroke_width=7.5,stroke_opacity=1)
        def c_line(node1,node2): return Line(node1.get_center()+node1.radius*RIGHT,node2.get_center()+node2.radius*LEFT,stroke_width=5)
        
        input_node1=node().move_to(4*LEFT+UP)
        input_node2=node().next_to(input_node1,5*DOWN)

        middle_node=node().next_to(input_node1,DOWN+10*RIGHT)
        node1to=c_line(input_node1,middle_node)
        node2to=c_line(input_node2,middle_node)

        end_node=node().next_to(middle_node,10*RIGHT)
        nodemiddleto=c_line(middle_node,end_node)

        full_nn=VGroup(input_node1,input_node2,middle_node,node1to,node2to,end_node,nodemiddleto)

        self.camera.frame.move_to(middle_node).scale(0.6)
        self.camera.frame.save_state()
        self.play(Write(input_node1),Write(input_node2))
        self.play(AnimationGroup(*[Create(mob) for mob in [middle_node,node1to,node2to,end_node,nodemiddleto]],lag_ratio=.25))

        nnum=MathTex("0.7",font_size=17.5).move_to(input_node1)
        
        self.wait()
        self.play(self.camera.frame.animate.move_to(input_node1.get_center()+0.5*RIGHT+0.25*DOWN).scale(0.5))
        self.play(Write(nnum),input_node1.animate.set_fill(WHITE,opacity=0.25))
        self.wait()
        self.play(self.camera.frame.animate.move_to(node1to.get_center()+0.5*RIGHT+0.25*DOWN).scale(1.25),Unwrite(nnum),input_node1.animate.set_fill(WHITE,opacity=0))
        self.play(Indicate(node1to,color=BLUE,scale_factor=1.05))
        self.wait()
        self.play(Restore(self.camera.frame))
        self.wait()

        node1toflash=node1to.copy().set_color(BLUE)
        node2toflash=node2to.copy().set_color(BLUE)
        nodemiddletoflash=nodemiddleto.copy().set_color(BLUE)
        inputs=VGroup(input_node1,input_node2)
        first_wave=VGroup(node1toflash,node2toflash)

        self.play(AnimationGroup(Indicate(inputs,color=RED,scale_factor=1.025),
                                ShowPassingFlash(first_wave,time_width=0.5,run_time=1),
                                Flash(middle_node,flash_radius=0.25+2*SMALL_BUFF,
                                    rate_func=rush_from),
                                ShowPassingFlash(nodemiddletoflash,time_width=0.5,run_time=1)
                                ,Flash(end_node,
                                    flash_radius=0.25+2*SMALL_BUFF,rate_func=rush_from)
                                ,lag_ratio=1))
        self.wait()

        
        sigmoid=MathTex(r"\sigma(z)=\frac{1}{1+e^{-z}",font_size=70).move_to(self.camera.frame.get_center()+1.5*DOWN).scale(0.6)
        sigmoid_plane=NumberPlane(
            x_range=(-10, 10, 5),
            y_range=(0, 1, .5),
            x_length=5,
            y_length=1,
        ).scale(0.6).scale(2.5).next_to(sigmoid,3*UP)
        sigmoid_graph=sigmoid_plane.plot(lambda x:1/(1+np.exp(-x)))
        sigmag=VGroup(sigmoid,sigmoid_plane,sigmoid_graph)

        self.play(AnimationGroup(FadeOut(full_nn,shift=DOWN),FadeIn(sigmag,shift=DOWN)))
        self.wait()
        self.play(AnimationGroup(FadeIn(full_nn,shift=UP),FadeOut(sigmag,shift=UP)))
        self.wait()

        nodeval=MathTex("node value =",font_size=50).move_to(input_node2.get_center()+1.2*DOWN+RIGHT)
        a=MathTex("a =",font_size=50).move_to(nodeval)
        z=MathTex("w_{1}x_{1}+w_{2}x_{2}",font_size=50).next_to(a,RIGHT)
        sigma=MathTex(r"\sigma(w_{1}x_{1}+w_{2}x_{2}+b)",font_size=50).next_to(a,RIGHT-RIGHT*SMALL_BUFF)
        b=MathTex("+ b",font_size=50).next_to(z,RIGHT)
        b[0][1].set_color(PINK)
        bflash=middle_node.copy().set_color(PINK)

        self.play(self.camera.frame.animate.shift(DOWN))
        self.wait()
        self.play(Write(nodeval))
        self.wait()
        self.play(ReplacementTransform(nodeval,a))
        self.wait()
        self.play(Write(z))
        self.play(z[0][0].animate.set_color(BLUE),Create(first_wave[0]))
        self.play(z[0][5].animate.set_color(BLUE),Create(first_wave[1]))
        self.wait()
        self.play(Write(b),ShowPassingFlash(bflash,time_width=1,run_time=2))
        self.wait()
        self.play(AnimationGroup(ReplacementTransform(z,sigma),Flash(middle_node,flash_radius=0.25+2*SMALL_BUFF,rate_func=rush_from),lag_ratio=1),FadeOut(b),FadeOut(first_wave))
        self.wait()
        
        output=MathTex("a_{output}=",font_size=50).move_to(a)
        zo=MathTex("wa_{prev}+b",font_size=50).next_to(output,RIGHT)
        sigmao=MathTex("\sigma(wa_{prev}+b)",font_size=50).next_to(output,RIGHT)
        bflash_end=end_node.copy().set_color(PINK)
        lflash=nodemiddleto.copy().set_color(BLUE)

        self.play(ReplacementTransform(a,output),FadeOut(sigma))
        self.wait()
        self.play(AnimationGroup(Write(zo),ShowPassingFlash(lflash,time_width=0.5,run_time=1),
                                           ShowPassingFlash(bflash_end,time_width=1,run_time=2),lag_Ratio=1))
        self.wait()
        self.play(AnimationGroup(ReplacementTransform(zo,sigmao),
                                 Flash(end_node,flash_radius=0.25+2*SMALL_BUFF,rate_func=rush_from),lag_ratio=1))
        self.wait()

        randnodes=[MathTex("0.125",font_size=15).move_to(end_node),
                   MathTex(r"1/\pi",font_size=15).move_to(end_node),
                   MathTex(r"\ln(2)",font_size=15).move_to(end_node)]
        wantedval=Tex("want: 1",font_size=25).next_to(end_node,UP)

        self.play(self.camera.frame.animate.move_to(end_node).scale(0.4))
        self.remove(output,sigmao)
        self.play(Write(wantedval))
        self.wait()
        self.play(end_node.animate.set_fill(WHITE,0.25),Write(randnodes[0]))
        self.play(ReplacementTransform(randnodes[0],randnodes[1]))
        self.play(ReplacementTransform(randnodes[1],randnodes[2]))
        self.wait()
        self.play(Restore(self.camera.frame))
        self.wait()

        updatedval=MathTex("0.8",font_size=15).move_to(end_node)
        w_axis=NumberLine(x_range=[0,1,0.1],length=2).scale(1).next_to(node1to,0.5*UP+0.5*RIGHT).shift(LEFT)
        w_text=MathTex("w",font_size=25).next_to(w_axis,LEFT)
        w_dot=Dot(w_axis.n2p(0.4),color=BLUE).scale(0.75)
        w_line=Line(w_dot.get_center(),w_dot.get_center(),color=BLUE)
        better=Tex("Better Prediction!",color=GREEN,font_size=45).next_to(nodemiddleto,4*DOWN)

        self.play(Write(w_axis),Write(w_text),Write(w_dot),Create(first_wave[0]))
        self.wait()
        self.play(w_dot.animate.move_to(w_axis.n2p(0.5)),
                    w_line.animate.put_start_and_end_on(w_dot.get_center(),w_axis.n2p(0.5)))
        self.play(ReplacementTransform(randnodes[2],updatedval),Write(better))
        self.wait()
        
        df_dw=MathTex(r"\frac{df}{dw}>0",font_size=50).move_to(input_node2.get_center()+1.2*DOWN+1.5*RIGHT)
        imp=MathTex("\\implies f",font_size=50).next_to(df_dw,RIGHT)
        f_inc=Tex("is inc.",font_size=50).next_to(imp,RIGHT)

        self.play(self.camera.frame.animate.shift(DOWN),end_node.animate.set_fill(color=WHITE,opacity=0),
                  *[FadeOut(mob) for mob in [updatedval,wantedval,first_wave[0],better,w_axis,w_text,w_line,w_dot]])
        self.play(Write(df_dw))
        self.wait()
        self.play(AnimationGroup(Write(imp),Write(f_inc),lag_ratio=0.5))
        self.wait()


        