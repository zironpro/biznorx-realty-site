// Tiny static server for local preview of site/: node serve.js [port]
const http = require('http'), fs = require('fs'), path = require('path');
const root = path.join(__dirname, 'site'), port = +process.argv[2] || 5186;
const types = { '.html': 'text/html; charset=utf-8', '.css': 'text/css', '.js': 'text/javascript', '.svg': 'image/svg+xml', '.png': 'image/png', '.webp': 'image/webp', '.xml': 'application/xml', '.txt': 'text/plain', '.jpg': 'image/jpeg', '.xml': 'application/xml' };
http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split('?')[0]);
  if (p.endsWith('/')) p += 'index.html';
  const f = path.join(root, path.normalize(p));
  if (!f.startsWith(root)) return res.writeHead(403).end();
  fs.readFile(f, (err, data) => {
    if (err) return fs.readFile(path.join(root, '404.html'), (e2, nf) => res.writeHead(404, { 'Content-Type': types['.html'] }).end(nf || 'Not found'));
    res.writeHead(200, { 'Content-Type': types[path.extname(f)] || 'application/octet-stream', 'Cache-Control': 'no-store' }).end(data);
  });
}).listen(port, () => console.log('http://localhost:' + port));
