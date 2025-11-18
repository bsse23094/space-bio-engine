import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../core/services/api.service';
import { LoadingComponent } from '../../shared/loading/loading.component';

@Component({
  selector: 'app-search',
  standalone: true,
  imports: [CommonModule, FormsModule, LoadingComponent],
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss']
})
export class SearchComponent {
  query = '';
  results: any[] = [];
  loading = false;
  error: string | null = null;
  searchTime: number = 0;

  constructor(private api: ApiService) {}

  search() {
    if (!this.query.trim()) {
      this.error = 'please enter a search query';
      return;
    }
    
    this.loading = true;
    this.error = null;
    this.results = [];
    
    this.api.searchArticles(this.query, 20).subscribe({
      next: (res) => {
        console.log('Search response:', res);
        this.results = res.articles || [];
        this.searchTime = res.search_time_ms || 0;
        this.loading = false;
        
        if (this.results.length === 0) {
          this.error = null; // Will show empty state instead
        }
      },
      error: (err) => {
        console.error('Search error:', err);
        this.error = 'search failed - please try again';
        this.loading = false;
        this.results = [];
      }
    });
  }
}
