const fs = require('fs');
const path = require('path');
const { createCanvas } = require('canvas');

const WIDTH = 600;
const HEIGHT = 800;

const publicDir = path.join(process.cwd(), 'public', 'images');
const dataDir = path.join(process.cwd(), 'data', 'images');

if (!fs.existsSync(publicDir)) fs.mkdirSync(publicDir, { recursive: true });
if (!fs.existsSync(dataDir)) fs.mkdirSync(dataDir, { recursive: true });

function addFabricTexture(ctx, type = 'silk', baseAlpha = 0.08) {
  ctx.save();
  ctx.strokeStyle = `rgba(255, 255, 255, ${baseAlpha})`;
  ctx.lineWidth = 1;
  const step = type === 'coarse' ? 4 : 2;
  for (let y = 0; y < HEIGHT; y += step) {
    ctx.beginPath();
    ctx.moveTo(0, y);
    ctx.lineTo(WIDTH, y);
    ctx.stroke();
  }
  ctx.strokeStyle = `rgba(0, 0, 0, ${baseAlpha * 0.7})`;
  for (let x = 0; x < WIDTH; x += step) {
    ctx.beginPath();
    ctx.moveTo(x, 0);
    ctx.lineTo(x, HEIGHT);
    ctx.stroke();
  }
  ctx.restore();
}

function drawGoldZariBorder(ctx, x, y, w, h, isVertical = false, isSilver = false) {
  ctx.save();
  const grad = isVertical
    ? ctx.createLinearGradient(x, y, x + w, y)
    : ctx.createLinearGradient(x, y, x, y + h);

  if (isSilver) {
    grad.addColorStop(0, '#CBD5E1');
    grad.addColorStop(0.3, '#F8FAFC');
    grad.addColorStop(0.5, '#94A3B8');
    grad.addColorStop(0.8, '#E2E8F0');
    grad.addColorStop(1, '#64748B');
  } else {
    grad.addColorStop(0, '#B45309');
    grad.addColorStop(0.2, '#F59E0B');
    grad.addColorStop(0.5, '#FEF08A');
    grad.addColorStop(0.7, '#D97706');
    grad.addColorStop(1, '#92400E');
  }

  ctx.fillStyle = grad;
  ctx.fillRect(x, y, w, h);

  // Border micro motifs
  ctx.strokeStyle = isSilver ? 'rgba(51, 65, 85, 0.4)' : 'rgba(120, 53, 15, 0.5)';
  ctx.lineWidth = 1.5;

  if (isVertical) {
    for (let py = y + 10; py < y + h - 10; py += 25) {
      // Diamond / temple spike
      ctx.beginPath();
      ctx.moveTo(x + w / 2, py - 8);
      ctx.lineTo(x + w - 4, py);
      ctx.lineTo(x + w / 2, py + 8);
      ctx.lineTo(x + 4, py);
      ctx.closePath();
      ctx.stroke();
    }
  } else {
    for (let px = x + 10; px < x + w - 10; px += 25) {
      ctx.beginPath();
      ctx.moveTo(px, y + h / 2 - 8);
      ctx.lineTo(px + 8, y + h - 4);
      ctx.lineTo(px, y + h / 2 + 8);
      ctx.lineTo(px - 8, y + h - 4);
      ctx.closePath();
      ctx.stroke();
    }
  }
  ctx.restore();
}

function drawZariButta(ctx, cx, cy, radius, isSilver = false) {
  ctx.save();
  ctx.fillStyle = isSilver ? '#E2E8F0' : '#FCD34D';
  ctx.strokeStyle = isSilver ? '#94A3B8' : '#B45309';
  ctx.lineWidth = 1;

  ctx.beginPath();
  ctx.arc(cx, cy, radius, 0, Math.PI * 2);
  ctx.fill();
  ctx.stroke();

  // Petals
  for (let a = 0; a < Math.PI * 2; a += Math.PI / 4) {
    const px = cx + Math.cos(a) * (radius + 3);
    const py = cy + Math.sin(a) * (radius + 3);
    ctx.beginPath();
    ctx.arc(px, py, radius * 0.35, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
  }
  ctx.restore();
}

function drawTempleBorder(ctx, y, h, width, color = '#FFD700', bgBorder = '#991B1B') {
  ctx.save();
  ctx.fillStyle = bgBorder;
  ctx.fillRect(0, y, width, h);

  ctx.fillStyle = color;
  const triangleW = 20;
  const triangleH = h * 0.45;
  for (let px = 0; px < width; px += triangleW) {
    ctx.beginPath();
    ctx.moveTo(px, y + h);
    ctx.lineTo(px + triangleW / 2, y + h - triangleH);
    ctx.lineTo(px + triangleW, y + h);
    ctx.closePath();
    ctx.fill();

    // Inverted top triangle
    ctx.beginPath();
    ctx.moveTo(px, y);
    ctx.lineTo(px + triangleW / 2, y + triangleH);
    ctx.lineTo(px + triangleW, y);
    ctx.closePath();
    ctx.fill();
  }
  ctx.restore();
}

const SAREE_RENDERERS = {
  // 1. Banarasi Crimson Red
  'banarasi_crimson_red_gold_zari_brocade.jpg': (ctx) => {
    // Crimson body with soft luxury gradient
    const grad = ctx.createLinearGradient(0, 0, WIDTH, HEIGHT);
    grad.addColorStop(0, '#991B1B');
    grad.addColorStop(0.5, '#7F1D1D');
    grad.addColorStop(1, '#5C0F15');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, WIDTH, HEIGHT);
    addFabricTexture(ctx, 'silk', 0.1);

    // Floral Jaal Brocade across body
    ctx.strokeStyle = 'rgba(253, 224, 71, 0.45)';
    ctx.lineWidth = 1.2;
    for (let r = 80; r < 520; r += 45) {
      for (let c = 40; c < WIDTH - 40; c += 45) {
        drawZariButta(ctx, c + ((r % 90 === 0) ? 22 : 0), r, 6, false);
      }
    }

    // Top Border
    drawGoldZariBorder(ctx, 0, 0, WIDTH, 35, false, false);

    // Bottom Border
    drawGoldZariBorder(ctx, 0, HEIGHT - 55, WIDTH, 55, false, false);

    // Pallu (Right or Bottom side)
    const palluGrad = ctx.createLinearGradient(0, 540, 0, HEIGHT - 55);
    palluGrad.addColorStop(0, '#B45309');
    palluGrad.addColorStop(0.5, '#D97706');
    palluGrad.addColorStop(1, '#92400E');
    ctx.fillStyle = palluGrad;
    ctx.fillRect(0, 540, WIDTH, 205);

    // Grand Kalga & Paisley Motifs in Pallu
    for (let x = 40; x < WIDTH; x += 70) {
      ctx.fillStyle = '#FEF08A';
      ctx.beginPath();
      ctx.arc(x, 620, 18, 0, Math.PI * 2);
      ctx.fill();
      ctx.beginPath();
      ctx.moveTo(x, 600);
      ctx.quadraticCurveTo(x + 25, 570, x + 5, 555);
      ctx.quadraticCurveTo(x - 10, 580, x, 600);
      ctx.fill();
    }
  },

  // 2. Banarasi Navy Blue Silver Zari
  'banarasi_royal_navy_blue_silver_zari.jpg': (ctx) => {
    const grad = ctx.createLinearGradient(0, 0, WIDTH, HEIGHT);
    grad.addColorStop(0, '#1E1B4B');
    grad.addColorStop(0.4, '#0F172A');
    grad.addColorStop(1, '#172554');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, WIDTH, HEIGHT);
    addFabricTexture(ctx, 'silk', 0.12);

    // Silver Bootis
    for (let r = 80; r < 530; r += 45) {
      for (let c = 40; c < WIDTH - 40; c += 45) {
        drawZariButta(ctx, c + ((r % 90 === 0) ? 22 : 0), r, 5, true);
      }
    }

    drawGoldZariBorder(ctx, 0, 0, WIDTH, 35, false, true);
    drawGoldZariBorder(ctx, 0, HEIGHT - 55, WIDTH, 55, false, true);

    // Silver Pallu
    const palluGrad = ctx.createLinearGradient(0, 540, 0, HEIGHT - 55);
    palluGrad.addColorStop(0, '#94A3B8');
    palluGrad.addColorStop(0.5, '#E2E8F0');
    palluGrad.addColorStop(1, '#64748B');
    ctx.fillStyle = palluGrad;
    ctx.fillRect(0, 540, WIDTH, 205);

    ctx.strokeStyle = '#334155';
    ctx.lineWidth = 1.5;
    for (let x = 0; x < WIDTH; x += 30) {
      ctx.beginPath();
      ctx.moveTo(x, 540);
      ctx.lineTo(x + 15, 640);
      ctx.lineTo(x + 30, 540);
      ctx.stroke();
    }
  },

  // 3. Kanjeevaram Emerald Green Ruby Red
  'kanjeevaram_emerald_green_ruby_red_border.jpg': (ctx) => {
    // Body: Emerald Green
    const grad = ctx.createLinearGradient(0, 0, WIDTH, HEIGHT);
    grad.addColorStop(0, '#064E3B');
    grad.addColorStop(0.5, '#047857');
    grad.addColorStop(1, '#065F46');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, WIDTH, HEIGHT);
    addFabricTexture(ctx, 'silk', 0.1);

    // Gold zari checks/dots on body
    ctx.fillStyle = 'rgba(253, 224, 71, 0.4)';
    for (let y = 80; y < 520; y += 30) {
      for (let x = 40; x < WIDTH - 40; x += 30) {
        ctx.fillRect(x, y, 3, 3);
      }
    }

    // Contrasting Ruby Red Korvai Temple Borders
    drawTempleBorder(ctx, 0, 45, WIDTH, '#FCD34D', '#991B1B');
    drawTempleBorder(ctx, HEIGHT - 70, 70, WIDTH, '#FCD34D', '#991B1B');

    // Heavy Ruby Red & Gold Zari Pallu
    ctx.fillStyle = '#881337';
    ctx.fillRect(0, 520, WIDTH, 210);
    drawGoldZariBorder(ctx, 0, 530, WIDTH, 35, false, false);
    drawGoldZariBorder(ctx, 0, 600, WIDTH, 50, false, false);
    drawGoldZariBorder(ctx, 0, 680, WIDTH, 40, false, false);
  },

  // 4. Kanjeevaram Mustard Gold Peacock Blue
  'kanjeevaram_mustard_gold_peacock_blue_border.jpg': (ctx) => {
    // Body: Mustard Gold
    const grad = ctx.createLinearGradient(0, 0, WIDTH, HEIGHT);
    grad.addColorStop(0, '#D97706');
    grad.addColorStop(0.5, '#F59E0B');
    grad.addColorStop(1, '#B45309');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, WIDTH, HEIGHT);
    addFabricTexture(ctx, 'silk', 0.1);

    // Zari brocade subtle diamond grid
    ctx.strokeStyle = 'rgba(254, 240, 138, 0.35)';
    ctx.lineWidth = 1;
    for (let x = -HEIGHT; x < WIDTH + HEIGHT; x += 35) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x + HEIGHT, HEIGHT);
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(x + HEIGHT, 0);
      ctx.lineTo(x, HEIGHT);
      ctx.stroke();
    }

    // Peacock Blue Korvai Borders
    drawTempleBorder(ctx, 0, 45, WIDTH, '#FCD34D', '#0369A1');
    drawTempleBorder(ctx, HEIGHT - 70, 70, WIDTH, '#FCD34D', '#0369A1');

    // Peacock Blue Pallu
    ctx.fillStyle = '#075985';
    ctx.fillRect(0, 520, WIDTH, 210);
    drawGoldZariBorder(ctx, 0, 540, WIDTH, 45, false, false);
    drawGoldZariBorder(ctx, 0, 610, WIDTH, 65, false, false);
  },

  // 5. Bandhani Ruby Red Yellow Dots
  'bandhani_traditional_ruby_red_yellow_dots.jpg': (ctx) => {
    ctx.fillStyle = '#DC2626';
    ctx.fillRect(0, 0, WIDTH, HEIGHT);
    addFabricTexture(ctx, 'coarse', 0.06);

    // Clustered Bandhani Ring Dots
    for (let cy = 50; cy < HEIGHT - 50; cy += 40) {
      for (let cx = 40; cx < WIDTH - 40; cx += 40) {
        // Outer yellow ring
        ctx.fillStyle = '#FBBF24';
        ctx.beginPath();
        ctx.arc(cx, cy, 7, 0, Math.PI * 2);
        ctx.fill();

        // Inner white dot
        ctx.fillStyle = '#FFFFFF';
        ctx.beginPath();
        ctx.arc(cx, cy, 3, 0, Math.PI * 2);
        ctx.fill();
      }
    }

    // Gota Patti Gold Border
    drawGoldZariBorder(ctx, 0, 0, WIDTH, 25, false, false);
    drawGoldZariBorder(ctx, 0, HEIGHT - 35, WIDTH, 35, false, false);
  },

  // 6. Bandhani Deep Maroon White Leheriya
  'bandhani_deep_maroon_white_leheriya.jpg': (ctx) => {
    ctx.fillStyle = '#7F1D1D';
    ctx.fillRect(0, 0, WIDTH, HEIGHT);
    addFabricTexture(ctx, 'coarse', 0.08);

    // Diagonal Leheriya Waves
    ctx.lineWidth = 6;
    for (let x = -HEIGHT; x < WIDTH + HEIGHT; x += 30) {
      ctx.strokeStyle = 'rgba(255, 255, 255, 0.85)';
      ctx.beginPath();
      for (let y = 0; y < HEIGHT; y += 10) {
        const xOffset = Math.sin(y / 20) * 8;
        const curX = x + y * 0.8 + xOffset;
        if (y === 0) ctx.moveTo(curX, y);
        else ctx.lineTo(curX, y);
      }
      ctx.stroke();

      // Thin gold companion wave
      ctx.strokeStyle = 'rgba(253, 224, 71, 0.7)';
      ctx.lineWidth = 2;
      ctx.stroke();
    }

    drawGoldZariBorder(ctx, 0, 0, WIDTH, 20, false, false);
    drawGoldZariBorder(ctx, 0, HEIGHT - 30, WIDTH, 30, false, false);
  },

  // 7. Chanderi Pastel Peach Silver Zari
  'chanderi_pastel_peach_silver_zari_booti.jpg': (ctx) => {
    const grad = ctx.createLinearGradient(0, 0, WIDTH, HEIGHT);
    grad.addColorStop(0, '#FED7AA');
    grad.addColorStop(0.5, '#FFEDD5');
    grad.addColorStop(1, '#FDBA74');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, WIDTH, HEIGHT);
    addFabricTexture(ctx, 'silk', 0.07);

    // Fine Silver Ashrafi Bootis
    for (let y = 60; y < HEIGHT - 60; y += 50) {
      for (let x = 40; x < WIDTH - 40; x += 50) {
        drawZariButta(ctx, x + ((y % 100 === 0) ? 25 : 0), y, 4, true);
      }
    }

    drawGoldZariBorder(ctx, 0, 0, WIDTH, 20, false, true);
    drawGoldZariBorder(ctx, 0, HEIGHT - 35, WIDTH, 35, false, true);
  },

  // 8. Chanderi Mint Green Geometric Zari
  'chanderi_mint_green_geometric_zari.jpg': (ctx) => {
    const grad = ctx.createLinearGradient(0, 0, WIDTH, HEIGHT);
    grad.addColorStop(0, '#A7F3D0');
    grad.addColorStop(0.5, '#D1FAE5');
    grad.addColorStop(1, '#6EE7B7');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, WIDTH, HEIGHT);
    addFabricTexture(ctx, 'silk', 0.07);

    // Soft Gold Geometric Diamond Grid
    ctx.strokeStyle = 'rgba(217, 119, 6, 0.4)';
    ctx.lineWidth = 1.2;
    for (let x = -HEIGHT; x < WIDTH + HEIGHT; x += 40) {
      ctx.beginPath();
      ctx.moveTo(x, 0);
      ctx.lineTo(x + HEIGHT, HEIGHT);
      ctx.stroke();
      ctx.beginPath();
      ctx.moveTo(x + HEIGHT, 0);
      ctx.lineTo(x, HEIGHT);
      ctx.stroke();
    }

    drawGoldZariBorder(ctx, 0, 0, WIDTH, 22, false, false);
    drawGoldZariBorder(ctx, 0, HEIGHT - 38, WIDTH, 38, false, false);
  },

  // 9. Kalamkari Natural Beige Tree of Life
  'kalamkari_natural_beige_tree_of_life_cotton.jpg': (ctx) => {
    ctx.fillStyle = '#F5F5DC';
    ctx.fillRect(0, 0, WIDTH, HEIGHT);
    addFabricTexture(ctx, 'coarse', 0.15);

    // Hand painted Tree of Life branches and leaves
    ctx.strokeStyle = '#78350F';
    ctx.lineWidth = 6;
    ctx.beginPath();
    ctx.moveTo(WIDTH / 2, HEIGHT - 80);
    ctx.bezierCurveTo(WIDTH / 2 - 40, 500, WIDTH / 2 + 50, 350, WIDTH / 2, 200);
    ctx.stroke();

    // Branches
    const branches = [
      [WIDTH / 2, 450, WIDTH / 2 - 120, 380],
      [WIDTH / 2, 400, WIDTH / 2 + 130, 320],
      [WIDTH / 2, 320, WIDTH / 2 - 140, 240],
      [WIDTH / 2, 260, WIDTH / 2 + 120, 180],
      [WIDTH / 2, 200, WIDTH / 2 - 80, 120],
      [WIDTH / 2, 200, WIDTH / 2 + 80, 110],
    ];

    ctx.lineWidth = 3.5;
    branches.forEach(([x1, y1, x2, y2]) => {
      ctx.beginPath();
      ctx.moveTo(x1, y1);
      ctx.quadraticCurveTo((x1 + x2) / 2 + 15, (y1 + y2) / 2, x2, y2);
      ctx.stroke();

      // Leaves and Flowers in Terracotta & Indigo
      for (let t = 0.3; t <= 1.0; t += 0.25) {
        const lx = x1 + (x2 - x1) * t;
        const ly = y1 + (y2 - y1) * t;
        ctx.fillStyle = t > 0.5 ? '#9A3412' : '#1E3A8A';
        ctx.beginPath();
        ctx.ellipse(lx, ly, 10, 5, Math.PI / 4, 0, Math.PI * 2);
        ctx.fill();
      }
    });

    // Terracotta spiked border
    drawTempleBorder(ctx, 0, 30, WIDTH, '#78350F', '#9A3412');
    drawTempleBorder(ctx, HEIGHT - 45, 45, WIDTH, '#78350F', '#9A3412');
  },

  // 10. Kalamkari Indigo Blue
  'kalamkari_indigo_blue_mythological_motifs.jpg': (ctx) => {
    ctx.fillStyle = '#1E3A8A';
    ctx.fillRect(0, 0, WIDTH, HEIGHT);
    addFabricTexture(ctx, 'coarse', 0.12);

    // Traditional block print motifs in beige/mustard
    ctx.fillStyle = '#FEF3C7';
    ctx.strokeStyle = '#D97706';
    ctx.lineWidth = 1;

    for (let y = 60; y < HEIGHT - 60; y += 70) {
      for (let x = 50; x < WIDTH - 50; x += 70) {
        ctx.beginPath();
        ctx.arc(x, y, 14, 0, Math.PI * 2);
        ctx.fill();
        ctx.stroke();

        ctx.beginPath();
        ctx.arc(x, y, 6, 0, Math.PI * 2);
        ctx.fillStyle = '#9A3412';
        ctx.fill();
        ctx.fillStyle = '#FEF3C7';
      }
    }

    drawTempleBorder(ctx, 0, 35, WIDTH, '#D97706', '#172554');
    drawTempleBorder(ctx, HEIGHT - 50, 50, WIDTH, '#D97706', '#172554');
  },

  // 11. Paithani Royal Purple Gold Peacock
  'paithani_royal_purple_gold_mor_peacock_pallu.jpg': (ctx) => {
    const grad = ctx.createLinearGradient(0, 0, WIDTH, HEIGHT);
    grad.addColorStop(0, '#581C87');
    grad.addColorStop(0.5, '#3B0764');
    grad.addColorStop(1, '#6B21A8');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, WIDTH, HEIGHT);
    addFabricTexture(ctx, 'silk', 0.1);

    // Fine gold zari buttas on body
    for (let r = 80; r < 500; r += 50) {
      for (let c = 40; c < WIDTH - 40; c += 50) {
        drawZariButta(ctx, c + ((r % 100 === 0) ? 25 : 0), r, 5, false);
      }
    }

    drawGoldZariBorder(ctx, 0, 0, WIDTH, 35, false, false);
    drawGoldZariBorder(ctx, 0, HEIGHT - 55, WIDTH, 55, false, false);

    // Grand Yeola Paithani Gold Tapestry Pallu with Peacocks
    const palluGrad = ctx.createLinearGradient(0, 510, 0, HEIGHT - 55);
    palluGrad.addColorStop(0, '#B45309');
    palluGrad.addColorStop(0.4, '#F59E0B');
    palluGrad.addColorStop(0.8, '#FCD34D');
    palluGrad.addColorStop(1, '#B45309');
    ctx.fillStyle = palluGrad;
    ctx.fillRect(0, 510, WIDTH, 235);

    // Colored Mor (Peacock) Motifs
    for (let px = 80; px < WIDTH; px += 140) {
      // Body
      ctx.fillStyle = '#0284C7';
      ctx.beginPath();
      ctx.ellipse(px, 620, 16, 26, -Math.PI / 6, 0, Math.PI * 2);
      ctx.fill();

      // Enamelled Crown & Neck
      ctx.fillStyle = '#059669';
      ctx.beginPath();
      ctx.arc(px + 10, 590, 8, 0, Math.PI * 2);
      ctx.fill();

      // Golden Tail Feathers
      ctx.strokeStyle = '#B91C1C';
      ctx.lineWidth = 2.5;
      for (let a = -0.8; a <= 0.8; a += 0.3) {
        ctx.beginPath();
        ctx.moveTo(px - 10, 630);
        ctx.lineTo(px - 40 + Math.cos(a) * 30, 610 + Math.sin(a) * 30);
        ctx.stroke();
      }
    }
  },

  // 12. Patola Double Ikat Maroon Black Elephant
  'patola_double_ikat_maroon_black_elephant.jpg': (ctx) => {
    ctx.fillStyle = '#881337';
    ctx.fillRect(0, 0, WIDTH, HEIGHT);
    addFabricTexture(ctx, 'silk', 0.12);

    // Geometric Double Ikat Grid
    const step = 60;
    for (let y = 60; y < HEIGHT - 60; y += step) {
      for (let x = 40; x < WIDTH - 40; x += step) {
        // Charcoal box
        ctx.fillStyle = '#0F172A';
        ctx.fillRect(x, y, step - 8, step - 8);

        // Gold & White Kunjar (Elephant) / Popat (Parrot) motif silhouette
        ctx.fillStyle = '#F59E0B';
        ctx.fillRect(x + 12, y + 15, 28, 18);
        ctx.fillRect(x + 16, y + 33, 6, 12);
        ctx.fillRect(x + 32, y + 33, 6, 12);
        ctx.fillStyle = '#FFFFFF';
        ctx.fillRect(x + 10, y + 20, 5, 10);
      }
    }

    drawTempleBorder(ctx, 0, 40, WIDTH, '#F59E0B', '#0F172A');
    drawTempleBorder(ctx, HEIGHT - 55, 55, WIDTH, '#F59E0B', '#0F172A');
  },

  // 13. Patola Emerald & Mustard
  'patola_emerald_and_mustard_geometric_parrot.jpg': (ctx) => {
    ctx.fillStyle = '#065F46';
    ctx.fillRect(0, 0, WIDTH, HEIGHT);
    addFabricTexture(ctx, 'silk', 0.12);

    // Geometric Diamond Ikat Grid
    const step = 65;
    for (let y = 60; y < HEIGHT - 60; y += step) {
      for (let x = 40; x < WIDTH - 40; x += step) {
        // Mustard diamond
        ctx.fillStyle = '#D97706';
        ctx.beginPath();
        ctx.moveTo(x + step / 2, y);
        ctx.lineTo(x + step, y + step / 2);
        ctx.lineTo(x + step / 2, y + step);
        ctx.lineTo(x, y + step / 2);
        ctx.closePath();
        ctx.fill();

        // Inner Crimson square
        ctx.fillStyle = '#BE123C';
        ctx.fillRect(x + step / 2 - 8, y + step / 2 - 8, 16, 16);
      }
    }

    drawTempleBorder(ctx, 0, 40, WIDTH, '#D97706', '#BE123C');
    drawTempleBorder(ctx, HEIGHT - 55, 55, WIDTH, '#D97706', '#BE123C');
  },

  // 14. Sambalpuri Ikat Terracotta
  'sambalpuri_ikat_terracotta_chevron_black_border.jpg': (ctx) => {
    ctx.fillStyle = '#9A3412';
    ctx.fillRect(0, 0, WIDTH, HEIGHT);
    addFabricTexture(ctx, 'coarse', 0.15);

    // White & Black Chevron Bandha Ikat
    ctx.lineWidth = 3.5;
    for (let y = 60; y < HEIGHT - 60; y += 35) {
      ctx.strokeStyle = '#FFFFFF';
      ctx.beginPath();
      for (let x = 0; x < WIDTH; x += 30) {
        ctx.lineTo(x, y);
        ctx.lineTo(x + 15, y - 12);
        ctx.lineTo(x + 30, y);
      }
      ctx.stroke();

      ctx.strokeStyle = '#000000';
      ctx.stroke();
    }

    // Black Fish & Shankha Border
    ctx.fillStyle = '#000000';
    ctx.fillRect(0, 0, WIDTH, 40);
    ctx.fillRect(0, HEIGHT - 60, WIDTH, 60);

    ctx.fillStyle = '#EA580C';
    for (let x = 20; x < WIDTH; x += 40) {
      ctx.beginPath();
      ctx.ellipse(x, 20, 10, 5, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.beginPath();
      ctx.ellipse(x, HEIGHT - 30, 12, 6, 0, 0, Math.PI * 2);
      ctx.fill();
    }
  },

  // 15. Tussar Silk Raw Golden Beige Kantha
  'tussar_silk_raw_golden_beige_kantha_embroidery.jpg': (ctx) => {
    ctx.fillStyle = '#CA8A04';
    ctx.fillRect(0, 0, WIDTH, HEIGHT);
    addFabricTexture(ctx, 'coarse', 0.2); // Slubby wild tussar texture

    // Hand Kantha Multicolor Running Stitches
    const stitchColors = ['#B91C1C', '#1E3A8A', '#15803D', '#78350F'];
    for (let y = 60; y < HEIGHT - 60; y += 25) {
      const col = stitchColors[(y / 25) % stitchColors.length];
      ctx.strokeStyle = col;
      ctx.lineWidth = 1.8;
      ctx.setLineDash([8, 6]);
      ctx.beginPath();
      ctx.moveTo(30, y);
      ctx.lineTo(WIDTH - 30, y);
      ctx.stroke();
    }
    ctx.setLineDash([]); // Reset

    drawGoldZariBorder(ctx, 0, 0, WIDTH, 25, false, false);
    drawGoldZariBorder(ctx, 0, HEIGHT - 45, WIDTH, 45, false, false);
  },

  // 16. Tussar Silk Rust Orange Tribal Weave
  'tussar_silk_rust_orange_tribal_weave.jpg': (ctx) => {
    ctx.fillStyle = '#C2410C';
    ctx.fillRect(0, 0, WIDTH, HEIGHT);
    addFabricTexture(ctx, 'coarse', 0.18);

    // Tribal Pit-loom geometric motifs
    ctx.fillStyle = '#7C2D12';
    for (let y = 80; y < HEIGHT - 80; y += 60) {
      for (let x = 40; x < WIDTH - 40; x += 60) {
        ctx.fillRect(x, y, 20, 20);
        ctx.fillStyle = '#FEF3C7';
        ctx.fillRect(x + 5, y + 5, 10, 10);
        ctx.fillStyle = '#7C2D12';
      }
    }

    drawGoldZariBorder(ctx, 0, 0, WIDTH, 28, false, false);
    drawGoldZariBorder(ctx, 0, HEIGHT - 45, WIDTH, 45, false, false);
  },

  // 17. Kasavu Kerala Off-White Gold Border
  'kasavu_kerala_offwhite_broad_gold_border.jpg': (ctx) => {
    // Crisp Ivory body
    ctx.fillStyle = '#FFFFF0';
    ctx.fillRect(0, 0, WIDTH, HEIGHT);
    addFabricTexture(ctx, 'silk', 0.05);

    // Top Gold Kara Border
    drawGoldZariBorder(ctx, 0, 0, WIDTH, 35, false, false);

    // Extra Broad Solid Gold Kara Border (Iconic Kasavu signature)
    drawGoldZariBorder(ctx, 0, HEIGHT - 110, WIDTH, 110, false, false);

    // Rich Gold Striped Kasavu Pallu
    for (let y = 520; y < HEIGHT - 120; y += 22) {
      drawGoldZariBorder(ctx, 0, y, WIDTH, 8, false, false);
    }
  },

  // 18. Georgette Rose Pink Botanical Print
  'georgette_rose_pink_botanical_print.jpg': (ctx) => {
    const grad = ctx.createLinearGradient(0, 0, WIDTH, HEIGHT);
    grad.addColorStop(0, '#FDA4AF');
    grad.addColorStop(0.5, '#FB7185');
    grad.addColorStop(1, '#F43F5E');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, WIDTH, HEIGHT);
    addFabricTexture(ctx, 'coarse', 0.05);

    // Watercolor Peony Blossoms & Foliage
    for (let y = 70; y < HEIGHT - 60; y += 85) {
      for (let x = 60; x < WIDTH - 50; x += 85) {
        // Peony
        ctx.fillStyle = 'rgba(255, 255, 255, 0.7)';
        ctx.beginPath();
        ctx.arc(x, y, 22, 0, Math.PI * 2);
        ctx.fill();

        ctx.fillStyle = 'rgba(244, 63, 94, 0.6)';
        ctx.beginPath();
        ctx.arc(x, y, 12, 0, Math.PI * 2);
        ctx.fill();

        // Sage Leaf
        ctx.fillStyle = 'rgba(134, 239, 172, 0.7)';
        ctx.beginPath();
        ctx.ellipse(x + 20, y + 12, 14, 6, Math.PI / 4, 0, Math.PI * 2);
        ctx.fill();
      }
    }

    // Scalloped Hem
    ctx.fillStyle = '#FFFFFF';
    for (let x = 0; x < WIDTH; x += 20) {
      ctx.beginPath();
      ctx.arc(x + 10, HEIGHT - 15, 10, 0, Math.PI);
      ctx.fill();
    }
  },

  // 19. Georgette Lavender Ombre Floral
  'georgette_lavender_ombre_floral_digital_print.jpg': (ctx) => {
    const grad = ctx.createLinearGradient(0, 0, 0, HEIGHT);
    grad.addColorStop(0, '#E9D5FF');
    grad.addColorStop(0.4, '#C084FC');
    grad.addColorStop(0.8, '#7E22CE');
    grad.addColorStop(1, '#581C87');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, WIDTH, HEIGHT);
    addFabricTexture(ctx, 'coarse', 0.05);

    // Micro Silver Sequins
    ctx.fillStyle = 'rgba(255, 255, 255, 0.85)';
    for (let y = 50; y < HEIGHT - 50; y += 30) {
      for (let x = 30; x < WIDTH - 30; x += 30) {
        ctx.fillRect(x + ((y % 60 === 0) ? 15 : 0), y, 2, 2);
      }
    }

    drawGoldZariBorder(ctx, 0, 0, WIDTH, 20, false, true);
    drawGoldZariBorder(ctx, 0, HEIGHT - 35, WIDTH, 35, false, true);
  },

  // 20. Organza Glass Tissue Powder Blue
  'organza_glass_tissue_powder_blue_scallop_zari.jpg': (ctx) => {
    const grad = ctx.createLinearGradient(0, 0, WIDTH, HEIGHT);
    grad.addColorStop(0, '#DBEAFE');
    grad.addColorStop(0.5, '#BFDBFE');
    grad.addColorStop(1, '#93C5FD');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, WIDTH, HEIGHT);
    addFabricTexture(ctx, 'silk', 0.06);

    // Glass sheen highlights
    const sheen = ctx.createLinearGradient(0, 0, WIDTH, HEIGHT);
    sheen.addColorStop(0, 'rgba(255, 255, 255, 0.35)');
    sheen.addColorStop(0.5, 'rgba(255, 255, 255, 0.0)');
    sheen.addColorStop(1, 'rgba(255, 255, 255, 0.35)');
    ctx.fillStyle = sheen;
    ctx.fillRect(0, 0, WIDTH, HEIGHT);

    // Scattered Silver Buttas
    for (let y = 60; y < HEIGHT - 60; y += 60) {
      for (let x = 40; x < WIDTH - 40; x += 60) {
        drawZariButta(ctx, x + ((y % 120 === 0) ? 30 : 0), y, 4, true);
      }
    }

    // Scalloped Silver Zari Border
    drawGoldZariBorder(ctx, 0, 0, WIDTH, 20, false, true);

    ctx.fillStyle = '#E2E8F0';
    for (let x = 0; x < WIDTH; x += 25) {
      ctx.beginPath();
      ctx.arc(x + 12.5, HEIGHT - 20, 12.5, 0, Math.PI);
      ctx.fill();
    }
  },
};

console.log('Generating high-resolution authentic saree images...');

Object.entries(SAREE_RENDERERS).forEach(([filename, renderFn]) => {
  const canvas = createCanvas(WIDTH, HEIGHT);
  const ctx = canvas.getContext('2d');

  renderFn(ctx);

  const buffer = canvas.toBuffer('image/jpeg', { quality: 0.95 });

  const pubPath = path.join(publicDir, filename);
  const datPath = path.join(dataDir, filename);

  fs.writeFileSync(pubPath, buffer);
  fs.writeFileSync(datPath, buffer);

  console.log(`Saved: ${filename} (${(buffer.length / 1024).toFixed(1)} KB)`);
});

console.log('All 20 saree images generated successfully!');
