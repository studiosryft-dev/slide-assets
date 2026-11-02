import numpy as np,wave
sr=44100;T=19.6;t=np.arange(int(sr*T))/sr;a=np.zeros_like(t)
def env(t0,t1,att=.05,rel=.1):
    e=np.zeros_like(t);m=(t>=t0)&(t<t1);x=t[m]-t0;d=t1-t0
    e[m]=np.minimum(1,x/att)*np.minimum(1,(d-x)/rel);return e
# ambient pad (lit): 0-7 and 12-19.6
pad=(np.sin(2*np.pi*110*t)+.6*np.sin(2*np.pi*165*t)+.4*np.sin(2*np.pi*220.5*t))*(.5+.5*np.sin(2*np.pi*.25*t))
a+=.06*pad*(env(0,7.0,.5,.02)+env(12.0,19.6,.05,1.2))
# riser during countdown
a+=.08*np.sin(2*np.pi*(220+180*np.clip(t-6,0,1)**2*t*0+ (t-6)*300)*t*.5)*env(6,7,.05,.01)
# power-cut thud at 7.0
m=t>=7;x=t-7;a+=np.where(m,.8*np.sin(2*np.pi*(55-20*np.minimum(x,.4))*x)*np.exp(-x*7),0)
# ticks at 8,9,10,11
for s in (8,9,10,11):
    m=(t>=s)&(t<s+.05);a+=np.where(m,.25*np.sin(2*np.pi*1800*(t-s))*np.exp(-(t-s)*90),0)
# power-on sweep at 12
x=t-12;m=(x>=0)&(x<.6);a+=np.where(m,.25*np.sin(2*np.pi*(150+900*x**1.5/.46)*x)*np.minimum(1,x/.02)*np.exp(-x*2),0)
# flicker buzz
a+=np.where((x>=0)&(x<.5),.1*np.sign(np.sin(2*np.pi*120*t)),0)
a/=max(1,np.abs(a).max()/.85)
w=wave.open('audio.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((a*32767).astype('<i2').tobytes());w.close()
