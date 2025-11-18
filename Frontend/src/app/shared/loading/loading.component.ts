import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-loading',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="loading-overlay">
      <div class="loading-content">
        <div class="spinner-container">
          <div class="spinner"></div>
          <div class="spinner-orbit"></div>
        </div>
        <p class="loading-text">loading</p>
      </div>
    </div>
  `,
  styles: [`
    .loading-overlay {
      position: fixed;
      top: 0;
      left: 0;
      width: 100vw;
      height: 100vh;
      background: rgba(0, 0, 0, 0.95);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 9999;
      backdrop-filter: blur(10px);
    }

    .loading-content {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 2rem;
    }

    .spinner-container {
      position: relative;
      width: 80px;
      height: 80px;
    }

    .spinner {
      position: absolute;
      width: 80px;
      height: 80px;
      border: 2px solid rgba(255, 255, 255, 0.1);
      border-top: 2px solid rgba(255, 255, 255, 0.8);
      border-radius: 50%;
      animation: spin 1s linear infinite;
    }

    .spinner-orbit {
      position: absolute;
      width: 60px;
      height: 60px;
      top: 10px;
      left: 10px;
      border: 1px solid rgba(255, 255, 255, 0.05);
      border-bottom: 1px solid rgba(255, 255, 255, 0.4);
      border-radius: 50%;
      animation: spin 1.5s linear infinite reverse;
    }

    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }

    .loading-text {
      font-family: 'Syncopate', sans-serif;
      font-size: 0.7rem;
      font-weight: 300;
      color: rgba(255, 255, 255, 0.5);
      letter-spacing: 0.3em;
      text-transform: lowercase;
      margin: 0;
      animation: pulse 2s ease-in-out infinite;
    }

    @keyframes pulse {
      0%, 100% { opacity: 0.3; }
      50% { opacity: 1; }
    }
  `]
})
export class LoadingComponent {}
