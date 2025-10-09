import { Component, OnInit } from '@angular/core';
import { ApiService } from '../../core/services/api.service';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss'],
  standalone: true,
  imports: [CommonModule, RouterModule]
})
export class DashboardComponent implements OnInit {
  stats: any = null;
  topicDistribution: any[] = [];
  temporalTrends: any[] = [];
  wordFrequencies: any[] = [];
  loading = false;
  error: string | null = null;

  constructor(private api: ApiService) {}

  ngOnInit(): void {
    this.loadAllData();
  }

  loadAllData() {
    this.loading = true;
    this.error = null;
    
    // Load statistics
    this.api.getStatistics().subscribe({
      next: (res) => {
        this.stats = res;
        this.loading = false;
      },
      error: (err) => {
        console.error(err);
        this.error = 'Failed to load statistics';
        this.loading = false;
      }
    });

    // Load topic distribution
    this.api.getTopicDistribution().subscribe({
      next: (res) => {
        this.topicDistribution = res;
      },
      error: (err) => console.error('Failed to load topic distribution', err)
    });

    // Load temporal trends
    this.api.getTemporalTrends().subscribe({
      next: (res) => {
        this.temporalTrends = res;
      },
      error: (err) => console.error('Failed to load temporal trends', err)
    });

    // Load word frequencies
    this.api.getWordFrequencies(15).subscribe({
      next: (res) => {
        this.wordFrequencies = res;
      },
      error: (err) => console.error('Failed to load word frequencies', err)
    });
  }

  getRelativeHeight(count: number): number {
    if (this.temporalTrends.length === 0) return 0;
    const maxCount = Math.max(...this.temporalTrends.map(t => t.article_count));
    return (count / maxCount) * 100;
  }

  getWordSize(frequency: number): number {
    if (this.wordFrequencies.length === 0) return 1;
    const maxFreq = Math.max(...this.wordFrequencies.map(w => w.frequency));
    const minSize = 0.9;
    const maxSize = 2.5;
    return minSize + (frequency / maxFreq) * (maxSize - minSize);
  }
}
