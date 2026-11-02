const {chromium}=require('playwright');const [a,b]=process.argv.slice(2).map(Number);
(async()=>{const br=await chromium.launch({args:['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist']});
const p=await br.newPage({viewport:{width:576,height:1024},deviceScaleFactor:1.25});
await p.goto('http://localhost:8123/');await p.waitForFunction('window.ready',null,{timeout:60000});
for(let f=a;f<b;f++){await p.evaluate(t=>window.render(t),f/30);await p.screenshot({path:`frames/f${String(f).padStart(4,'0')}.jpg`,type:'jpeg',quality:93})}
await br.close()})()
