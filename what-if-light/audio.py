import numpy as np,wave
sr=44100;T=13.5;n=int(sr*T);t=np.arange(n)/sr;rng=np.random.default_rng(3)
def lp(x,k):
    c=np.cumsum(np.insert(x,0,0));return (c[k:]-c[:-k])/k
def noise(k):
    return np.pad(lp(rng.standard_normal(n+k),k)[:n],(0,0))
def win(a,b,att=.03,rel=.05):
    e=np.zeros(n);m=(t>=a)&(t<b);x=t[m]-a;d=b-a;e[m]=np.minimum(1,x/att)*np.minimum(1,(d-x)/rel);return e
lit=win(0,3.0,.4,.01)+win(8.0,13.5,.05,1.0)*.6
amb=noise(60)*6+noise(400)*14   # city rumble / crowd wash
a=amb*lit*.5
# car horns at a few moments (beeps)
for s,f in [(.9,420),(1.6,370),(2.2,440),(3.15,400),(3.35,330)]:
    a+=.05*np.sign(np.sin(2*np.pi*f*t))*win(s,s+.35,.01,.05)*(1 if s<3.6 else 1)
# tire screech 3.2-4.6
sc=np.sin(2*np.pi*(2200+300*np.sin(2*np.pi*7*t))*t)*noise(3)*40
a+=.12*sc*win(3.2,4.6,.05,.5)
# power-cut thud at 3.0
x=np.clip(t-3,0,None);a+=np.where(t>=3,.9*np.sin(2*np.pi*(60-25*np.minimum(x,.4))*x)*np.exp(-x*6),0)
# faint distant horn + crowd gasp in dark
a+=.04*np.sign(np.sin(2*np.pi*390*t))*win(5.4,5.9,.01,.1)
a+=.05*noise(150)*20*win(3.3,4.2,.2,.5)
# ticks each second in the dark
for s in (4,5,6,7):
    a+=np.where((t>=s)&(t<s+.05),.2*np.sin(2*np.pi*1600*(t-s))*np.exp(-np.clip(t-s,0,.05)*90),0)
# power-on sweep at 8
x=np.clip(t-8,0,.6);a+=np.where((t>=8)&(t<8.6),.25*np.sin(2*np.pi*(150+1100*x)*x)*np.exp(-x*2),0)
a+=np.where((t>=8)&(t<8.55),.08*np.sign(np.sin(2*np.pi*120*t)),0)
# gentle low pad outro
a+=.03*np.sin(2*np.pi*110*t)*win(8.6,13.5,.5,1.0)
a/=max(1,np.abs(a).max()/.85)
w=wave.open('audio.wav','wb');w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((np.nan_to_num(a)*32767).astype('<i2').tobytes());w.close()
