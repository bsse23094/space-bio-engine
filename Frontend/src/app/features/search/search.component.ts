import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../../core/services/api.service';

@Component({
  selector: 'app-search',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './search.component.html',
  styleUrls: ['./search.component.scss']
})
export class SearchComponent {
  query = '';
  results: any[] = [];
  loading = false;
  error: string | null = null;

  constructor(private api: ApiService) {}

  search() {
    if (!this.query.trim()) return;
    this.loading = true;
    this.api.searchArticles(this.query).subscribe({
      next: (res) => {
        this.results = res;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Search failed';
        this.loading = false;
      }
    });
  }
}
