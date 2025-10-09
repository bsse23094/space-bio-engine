import { Component, AfterViewInit } from '@angular/core';
import { NavbarComponent } from './shared/navbar.component';
import { FooterComponent } from './shared/footer/footer.component';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [NavbarComponent, FooterComponent, RouterModule],
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements AfterViewInit {
  ngAfterViewInit() {
    // Create stars
    const starsContainer = document.getElementById('stars');
    if (starsContainer) {
      for (let i = 0; i < 120; i++) {
        const star = document.createElement('div');
        star.className = 'star';
        star.style.top = Math.random() * 100 + 'vh';
        star.style.left = Math.random() * 100 + 'vw';
        star.style.opacity = (0.5 + Math.random() * 0.5).toString();
        star.style.width = star.style.height = (1 + Math.random() * 2) + 'px';
        starsContainer.appendChild(star);
      }
    }

    // Create glowing lines
    const glowLinesContainer = document.getElementById('glowLines');
    if (glowLinesContainer) {
      setInterval(() => {
        const line = document.createElement('div');
        line.className = 'glow-line';
        line.style.top = Math.random() * 100 + '%';
        line.style.width = (30 + Math.random() * 40) + '%';
        line.style.animationDelay = Math.random() * 2 + 's';
        glowLinesContainer.appendChild(line);

        setTimeout(() => line.remove(), 10000);
      }, 3000);
    }
  }
}
