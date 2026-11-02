const http=require('http'),fs=require('fs'),path=require('path');
const root=__dirname,three=path.join(root,'node_modules/three');
http.createServer((q,r)=>{let u=q.url.split('?')[0];let f;
 if(u==='/'||u==='/index.html')f=path.join(root,'index.html');
 else if(u==='/three.module.js')f=path.join(three,'build/three.module.js');
 else if(u.startsWith('/addons/'))f=path.join(three,'examples/jsm',u.slice(8));
 else if(u==='/three.core.js')f=path.join(three,'build/three.core.js');
 if(!f||!fs.existsSync(f)){r.writeHead(404);return r.end()}
 r.writeHead(200,{'Content-Type':f.endsWith('.html')?'text/html':'text/javascript'});r.end(fs.readFileSync(f))}).listen(8123,()=>console.log('up'));
