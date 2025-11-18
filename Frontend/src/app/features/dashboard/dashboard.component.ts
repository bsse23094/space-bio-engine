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
        console.log('Stats loaded successfully:', res);
        this.stats = res;
        this.loading = false;
      },
      error: (err) => {
        console.error('Stats error:', err);
        this.error = `Stats error: ${err.message || err.error?.detail || 'Unknown error'}`;
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
    if (this.topicDistribution.length === 0) return 0;
    const maxCount = Math.max(...this.topicDistribution.map(t => t.article_count || 0));
    if (maxCount === 0) return 0;
    return (count / maxCount) * 100;
  }

  getWordSize(frequency: number): number {
    if (this.wordFrequencies.length === 0) return 1;
    const maxFreq = Math.max(...this.wordFrequencies.map(w => w.frequency));
    const minSize = 0.7;
    const maxSize = 1.8;
    return minSize + (frequency / maxFreq) * (maxSize - minSize);
  }

  getPercentage(value: number, total: number): number {
    if (!value || !total || total === 0) return 0;
    return (value / total) * 100;
  }

  getGraphPoints(): string {
    if (this.topicDistribution.length === 0) return '';
    
    const topics = this.topicDistribution.slice(0, 8);
    if (topics.length === 0) return '';
    
    const points = topics.map((topic, index) => {
      // Calculate x position based on column spacing
      const x = ((index + 0.5) / topics.length) * 100;
      // Calculate y position (inverted because SVG coordinates start from top)
      const height = this.getRelativeHeight(topic.article_count);
      const y = 100 - height;
      return `${x},${y}`;
    }).join(' ');
    
    return points;
  }
}
