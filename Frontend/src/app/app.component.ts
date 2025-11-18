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
    this.createStarfield();
  }

  createStarfield() {
    const starfield = document.getElementById('starfield');
    if (!starfield) return;

    // Create static stars
    for (let i = 0; i < 200; i++) {
      const star = document.createElement('div');
      const size = Math.random();
      
      if (size < 0.6) {
        star.className = 'star small';
      } else if (size < 0.9) {
        star.className = 'star medium';
      } else {
        star.className = 'star large';
      }
      
      star.style.top = Math.random() * 100 + '%';
      star.style.left = Math.random() * 100 + '%';
      star.style.animationDelay = Math.random() * 3 + 's';
      star.style.animationDuration = (2 + Math.random() * 3) + 's';
      
      starfield.appendChild(star);
    }

    // Create shooting stars periodically
    setInterval(() => {
      const shootingStar = document.createElement('div');
      shootingStar.className = 'shooting-star';
      shootingStar.style.top = Math.random() * 50 + '%';
      shootingStar.style.left = Math.random() * 100 + '%';
      shootingStar.style.animationDuration = (2 + Math.random() * 2) + 's';
      
      starfield.appendChild(shootingStar);
      
      setTimeout(() => shootingStar.remove(), 3000);
    }, 8000);
  }
}
