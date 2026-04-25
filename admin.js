const express = require('express');
const cors = require('cors');
const fs = require('fs');
const path = require('path');
const cheerio = require('cheerio');
const session = require('express-session');

const app = express();
const PORT = 3000;
const BASE_DIR = path.join(__dirname);

app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Setup Session
app.use(session({
    secret: 'ichibot-admin-secret-2026',
    resave: false,
    saveUninitialized: false,
    cookie: { secure: false, maxAge: 24 * 60 * 60 * 1000 } // 1 day
}));

// Admin credentials (You can change these later)
const ADMIN_USER = 'admin';
const ADMIN_PASS = 'ichibot123';

// Auth Middleware
function requireAuth(req, res, next) {
    if (req.session.loggedIn) {
        next();
    } else {
        // If it's an API request, return 401 JSON
        if (req.path.startsWith('/api/')) {
            return res.status(401).json({ error: 'Unauthorized', redirect: '/login' });
        }
        res.redirect('/login');
    }
}

// Routes for Login
app.get('/login', (req, res) => {
    if (req.session.loggedIn) return res.redirect('/admin');
    
    const errorMsg = req.query.error ? '<div style="color: #ff4757; margin-bottom: 16px; text-align: center;">Username atau password salah!</div>' : '';
    
    res.send(`
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Login Admin - Ichibot Robotics</title>
        <style>
            :root { --bg: #0a0a0a; --glass: rgba(15, 15, 15, 0.7); --border: rgba(255, 255, 255, 0.1); --text: #f0f0f0; --accent: #ff0033; }
            body { background: var(--bg); color: var(--text); font-family: 'Inter', sans-serif; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }
            .login-card { background: var(--glass); padding: 40px; border-radius: 16px; border: 1px solid var(--border); box-shadow: 0 20px 40px rgba(0,0,0,0.5); width: 100%; max-width: 400px; backdrop-filter: blur(10px); }
            h2 { text-align: center; margin-top: 0; margin-bottom: 30px; letter-spacing: 2px; }
            .form-group { margin-bottom: 20px; }
            label { display: block; margin-bottom: 8px; font-size: 0.9rem; color: #a0a0a0; }
            input { width: 100%; padding: 12px 16px; background: rgba(255,255,255,0.05); border: 1px solid var(--border); border-radius: 8px; color: white; font-size: 1rem; box-sizing: border-box; outline: none; }
            input:focus { border-color: var(--accent); }
            button { width: 100%; padding: 14px; background: var(--accent); color: white; border: none; border-radius: 8px; font-size: 1rem; font-weight: 600; cursor: pointer; transition: 0.3s; }
            button:hover { background: #d00028; }
        </style>
    </head>
    <body>
        <div class="login-card">
            <h2>ICHIBOT ADMIN</h2>
            ${errorMsg}
            <form method="POST" action="/login">
                <div class="form-group">
                    <label>Username</label>
                    <input type="text" name="username" required autofocus autocomplete="off">
                </div>
                <div class="form-group">
                    <label>Password</label>
                    <input type="password" name="password" required>
                </div>
                <button type="submit">LOGIN</button>
            </form>
        </div>
    </body>
    </html>
    `);
});

app.post('/login', (req, res) => {
    const { username, password } = req.body;
    if (username === ADMIN_USER && password === ADMIN_PASS) {
        req.session.loggedIn = true;
        res.redirect('/admin');
    } else {
        res.redirect('/login?error=1');
    }
});

app.get('/logout', (req, res) => {
    req.session.destroy();
    res.redirect('/login');
});

app.get('/', (req, res) => {
    res.redirect('/admin');
});

// Protect all admin routes below this point
app.use(requireAuth);

// Helper to get index file for a category
function getIndexFile(category) {
    if (category === 'products') return 'products.html';
    if (category === 'pelatihan') return 'pelatihan.html';
    if (category === 'blog') return 'blog.html';
    if (category === 'events') return 'events.html';
    return null;
}

// Serve the admin panel itself
app.get('/admin', (req, res) => {
    res.sendFile(path.join(__dirname, 'admin.html'));
});

// List all detail pages
app.get('/api/pages', (req, res) => {
    const files = fs.readdirSync(BASE_DIR);
    const pages = { products: [], pelatihan: [], blog: [], events: [] };

    files.forEach(file => {
        if (!file.endsWith('.html')) return;
        if (file.startsWith('product-') && file !== 'products.html' && file !== 'product-detail.html') pages.products.push(file);
        else if (file === 'product-detail.html') pages.products.push(file);
        else if (file.startsWith('pelatihan-') && file !== 'pelatihan.html') pages.pelatihan.push(file);
        else if (file.startsWith('achievement-') && file !== 'achievements.html') pages.blog.push(file);
        else if (file.startsWith('event-') && file !== 'events.html') pages.events.push(file);
    });
    res.json(pages);
});

// Get page details
app.get('/api/page', (req, res) => {
    const file = req.query.file;
    if (!file || !file.endsWith('.html')) return res.status(400).json({ error: 'Invalid file' });

    const filePath = path.join(BASE_DIR, file);
    if (!fs.existsSync(filePath)) return res.status(404).json({ error: 'File not found' });

    const content = fs.readFileSync(filePath, 'utf-8');
    const $ = cheerio.load(content);
    const data = { file };

    data.title = $('h1.detail-title').text().trim();
    data.image = $('.detail-image-wrap img').attr('src') || '';
    
    if (file.startsWith('product-') || file.startsWith('pelatihan-')) {
        data.type = file.startsWith('product-') ? 'products' : 'pelatihan';
        data.price = $('.detail-price').text().trim();
        data.price_coret = $('.detail-price-coret').text().trim();
        data.description = $('.detail-desc-text').first().text().trim();
        
        const waLink = $('a.btn-red[href^="https://wa.me/"]').attr('href');
        if (waLink) {
            try {
                const urlObj = new URL(waLink);
                data.whatsapp_text = urlObj.searchParams.get('text') || '';
            } catch(e) {}
        }

        data.specs1 = []; data.specs2 = [];
        const ulElements = $('ul.spec-list');
        if (ulElements.length > 0) $(ulElements[0]).find('li').each((i, el) => data.specs1.push($(el).text().trim()));
        if (ulElements.length > 1) $(ulElements[1]).find('li').each((i, el) => data.specs2.push($(el).text().trim()));
    } else if (file.startsWith('achievement-')) {
        data.type = 'blog';
        data.content = $('.blog-content').html() || '';
        const badgeEl = $('.detail-image-wrap').parent().prev().find('.badge').length ? $('.detail-image-wrap').parent().prev().find('.badge') : $('header .badge');
        data.badge = badgeEl.text().trim();
    } else if (file.startsWith('event-')) {
        data.type = 'events';
        data.description = $('.detail-desc-text').first().text().trim();
        data.badge = $('.detail-image-wrap .badge').text().trim();
        
        data.specs1 = []; data.specs2 = [];
        const ulElements = $('ul.spec-list');
        if (ulElements.length > 0) $(ulElements[0]).find('li').each((i, el) => data.specs1.push($(el).text().trim()));
        if (ulElements.length > 1) $(ulElements[1]).find('li').each((i, el) => data.specs2.push($(el).text().trim()));
    }

    res.json(data);
});

// Update page details
app.post('/api/page', (req, res) => {
    const file = req.body.file;
    const data = req.body;
    if (!file || !file.endsWith('.html')) return res.status(400).json({ error: 'Invalid file' });

    const filePath = path.join(BASE_DIR, file);
    if (!fs.existsSync(filePath)) return res.status(404).json({ error: 'File not found' });

    const content = fs.readFileSync(filePath, 'utf-8');
    const $ = cheerio.load(content);

    if (data.title) {
        $('h1.detail-title').text(data.title);
        $('title').text(`${data.title} — Ichibot Robotics`);
    }
    if (data.image) $('.detail-image-wrap img').attr('src', data.image);

    if (data.type === 'products' || data.type === 'pelatihan') {
        if (data.price !== undefined) $('.detail-price').text(data.price);
        if (data.price_coret !== undefined) $('.detail-price-coret').text(data.price_coret);
        if (data.description) $('.detail-desc-text').first().text(data.description);
        
        if (data.whatsapp_text) {
            const waBtn = $('a.btn-red[href^="https://wa.me/"]');
            waBtn.attr('href', `https://wa.me/6281234567890?text=${encodeURIComponent(data.whatsapp_text)}`);
        }

        if (data.specs1) {
            const ul1 = $('ul.spec-list').eq(0); ul1.empty();
            data.specs1.forEach(spec => ul1.append(`<li>${spec}</li>`));
        }
        if (data.specs2) {
            const ul2 = $('ul.spec-list').eq(1); ul2.empty();
            data.specs2.forEach(spec => ul2.append(`<li>${spec}</li>`));
        }
    } else if (data.type === 'blog') {
        if (data.content) $('.blog-content').html(data.content);
        if (data.badge) {
            const badgeEl = $('.detail-image-wrap').parent().prev().find('.badge').length ? $('.detail-image-wrap').parent().prev().find('.badge') : $('header .badge');
            badgeEl.text(data.badge);
        }
    } else if (data.type === 'events') {
        if (data.description) $('.detail-desc-text').first().text(data.description);
        if (data.badge) $('.detail-image-wrap .badge').text(data.badge);

        if (data.specs1) {
            const ul1 = $('ul.spec-list').eq(0); ul1.empty();
            data.specs1.forEach(spec => ul1.append(`<li>${spec}</li>`));
        }
        if (data.specs2) {
            const ul2 = $('ul.spec-list').eq(1); ul2.empty();
            data.specs2.forEach(spec => ul2.append(`<li>${spec}</li>`));
        }
    }

    fs.writeFileSync(filePath, $.html());

    const indexFile = getIndexFile(data.type);
    if (indexFile) {
        const idxPath = path.join(BASE_DIR, indexFile);
        const idxContent = fs.readFileSync(idxPath, 'utf-8');
        const $idx = cheerio.load(idxContent);
        
        const cardLink = $idx(`a[href="${file}"]`);
        if (cardLink.length > 0) {
            let cardWrap = cardLink.closest('.product-card-wrap');
            if (cardWrap.length === 0) cardWrap = cardLink.closest('.achievement-card-wrap');
            
            if (cardWrap.length > 0) {
                if (data.title) {
                    if (data.type === 'products' || data.type === 'pelatihan') cardWrap.find('.product-card-name').text(data.title);
                    else cardWrap.find('.achievement-card-title').text(data.title);
                }
                if (data.image) {
                    if (data.type === 'products' || data.type === 'pelatihan') cardWrap.find('.product-card-image img').attr('src', data.image);
                    else cardWrap.find('.achievement-card-image img').attr('src', data.image);
                }
                if (data.type === 'products' || data.type === 'pelatihan') {
                    if (data.price) cardWrap.find('.price-current').first().text(data.price);
                    if (data.price_coret) cardWrap.find('.price-original').text(data.price_coret);
                } else if (data.type === 'blog' || data.type === 'events') {
                    if (data.description) cardWrap.find('.achievement-card-desc').text(data.description);
                    if (data.type === 'blog' && data.badge) cardWrap.find('.badge').text(data.badge);
                }
                fs.writeFileSync(idxPath, $idx.html());
            }
        }
    }

    res.json({ success: true });
});

// Create new page
app.post('/api/create', (req, res) => {
    const { category, filename, title } = req.body;
    if (!filename || !filename.endsWith('.html')) return res.status(400).json({ error: 'Filename must end with .html' });
    
    let prefix = '';
    let templateFile = '';
    if (category === 'products') { prefix = 'product-'; templateFile = 'product-detail.html'; }
    else if (category === 'pelatihan') { prefix = 'pelatihan-'; templateFile = 'pelatihan-basic.html'; }
    else if (category === 'blog') { prefix = 'achievement-'; templateFile = 'achievement-ub.html'; }
    else if (category === 'events') { prefix = 'event-'; templateFile = 'event-its.html'; }
    else return res.status(400).json({ error: 'Invalid category' });

    if (!filename.startsWith(prefix)) return res.status(400).json({ error: `Filename must start with ${prefix}` });
    
    const filePath = path.join(BASE_DIR, filename);
    if (fs.existsSync(filePath)) return res.status(400).json({ error: 'File already exists' });

    let content = fs.readFileSync(path.join(BASE_DIR, templateFile), 'utf-8');
    const $ = cheerio.load(content);
    $('h1.detail-title').text(title);
    $('title').text(`${title} — Ichibot Robotics`);
    fs.writeFileSync(filePath, $.html());

    const indexFile = getIndexFile(category);
    if (indexFile) {
        const idxPath = path.join(BASE_DIR, indexFile);
        const idxContent = fs.readFileSync(idxPath, 'utf-8');
        const $idx = cheerio.load(idxContent);
        
        let newCard = '';
        if (category === 'products' || category === 'pelatihan') {
            newCard = `
            <div class="product-card-wrap animate-in" style="animation-delay: 0s;">
              <div class="glass-card product-card">
                <div class="product-card-image">
                  <img src="https://placehold.co/600x400/111111/444444?text=New" alt="${title}">
                  <span class="badge badge-white product-card-badge">Baru</span>
                </div>
                <div class="product-card-body">
                  <h3 class="product-card-name">${title}</h3>
                  <div class="product-card-price">
                    <span class="price-current">Rp 0</span>
                  </div>
                  <div class="product-card-actions">
                    <a href="${filename}" class="btn btn-ghost btn-sm">Detail</a>
                  </div>
                </div>
              </div>
            </div>`;
            $idx('.product-grid').first().prepend(newCard);
        } else if (category === 'blog' || category === 'events') {
            newCard = `
            <div class="achievement-card-wrap animate-in" data-category="berita" style="animation-delay: 0s;">
              <div class="glass-card achievement-card">
                <div class="achievement-card-image">
                  <img src="https://placehold.co/800x450/111111/444444?text=New" alt="${title}">
                </div>
                <div class="achievement-card-body">
                  <div class="achievement-card-meta">
                    <span class="badge badge-white">#Baru</span>
                    <span class="achievement-card-date">Hari Ini</span>
                  </div>
                  <h3 class="achievement-card-title">${title}</h3>
                  <p class="achievement-card-desc">Konten baru...</p>
                  <a href="${filename}" class="btn btn-ghost btn-sm" style="margin-top: 12px; width: 100%;">Baca Selengkapnya</a>
                </div>
              </div>
            </div>`;
            $idx('.masonry-grid').first().prepend(newCard);
        }
        fs.writeFileSync(idxPath, $idx.html());
    }

    res.json({ success: true, file: filename });
});

// Delete page
app.post('/api/delete', (req, res) => {
    const { category, file } = req.body;
    if (!file || !file.endsWith('.html')) return res.status(400).json({ error: 'Invalid file' });

    const filePath = path.join(BASE_DIR, file);
    if (fs.existsSync(filePath)) {
        fs.unlinkSync(filePath);
    }

    const indexFile = getIndexFile(category);
    if (indexFile) {
        const idxPath = path.join(BASE_DIR, indexFile);
        const idxContent = fs.readFileSync(idxPath, 'utf-8');
        const $idx = cheerio.load(idxContent);
        
        const cardLink = $idx(`a[href="${file}"]`);
        if (cardLink.length > 0) {
            let cardWrap = cardLink.closest('.product-card-wrap');
            if (cardWrap.length === 0) cardWrap = cardLink.closest('.achievement-card-wrap');
            if (cardWrap.length > 0) cardWrap.remove();
            fs.writeFileSync(idxPath, $idx.html());
        }
    }

    res.json({ success: true });
});

app.listen(PORT, () => {
    console.log(`Admin panel running on http://localhost:${PORT}/login`);
});
