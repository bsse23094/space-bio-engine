import { Component, HostListener } from '@angular/core';
import { RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss'],
  standalone: true,
  imports: [RouterModule, CommonModule]
})
export class NavbarComponent {
  menuOpen = false;
  compactNavbar = false;
  private lastScrollTop = 0;

  toggleMenu() { this.menuOpen = !this.menuOpen; }
  closeMenu() { this.menuOpen = false; }

  @HostListener('window:scroll', [])
  onWindowScroll() {
    const scrollTop = window.scrollY || document.documentElement.scrollTop;
    if (scrollTop > this.lastScrollTop && scrollTop > 100) {
      this.compactNavbar = true;
    } else if (scrollTop < this.lastScrollTop) {
      this.compactNavbar = false;
    }
    this.lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
  }
}
