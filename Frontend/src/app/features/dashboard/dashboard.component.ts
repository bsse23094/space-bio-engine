import { Component, OnInit, ViewChild, ElementRef, AfterViewInit } from '@angular/core';
import { ApiService } from '../../core/services/api.service';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { Chart, registerables } from 'chart.js';

Chart.register(...registerables);

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss'],
  standalone: true,
  imports: [CommonModule, RouterModule]
})
export class DashboardComponent implements OnInit, AfterViewInit {
  @ViewChild('lineChart') lineChartRef!: ElementRef<HTMLCanvasElement>;
  
  stats: any = null;
  topicDistribution: any[] = [];
  temporalTrends: any[] = [];
  wordFrequencies: any[] = [];
  loading = false;
  error: string | null = null;
  chart: Chart | null = null;

  constructor(private api: ApiService) {}

  ngOnInit(): void {
    this.loadAllData();
  }

  ngAfterViewInit(): void {
    // Chart will be created after data loads
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
        console.log('Topic distribution loaded:', res);
        setTimeout(() => {
          if (this.lineChartRef) {
            this.createChart();
          }
        }, 100);
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

  createChart(): void {
    if (this.chart) {
      this.chart.destroy();
    }

    if (!this.topicDistribution || this.topicDistribution.length === 0) {
      console.error('No topic distribution data available');
      return;
    }

    const topics = this.topicDistribution.slice(0, 8);
    const labels = topics.map(t => t.topic_name || `topic ${t.topic_id}`);
    const data = topics.map(t => t.article_count);

    console.log('Creating chart with labels:', labels, 'data:', data);

    const ctx = this.lineChartRef?.nativeElement?.getContext('2d');
    if (!ctx) {
      console.error('Canvas context not found');
      return;
    }

    this.chart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: labels,
        datasets: [{
          label: 'Articles',
          data: data,
          borderColor: 'rgba(255, 255, 255, 0.3)',
          borderWidth: 1.5,
          pointBackgroundColor: 'rgba(255, 255, 255, 0.8)',
          pointBorderColor: 'rgba(255, 255, 255, 0.8)',
          pointRadius: 4,
          pointHoverRadius: 6,
          pointHoverBackgroundColor: 'rgba(255, 255, 255, 1)',
          fill: false,
          tension: 0.3
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        animation: {
          duration: 1800,
          easing: 'easeInOutQuart',
          delay: (context) => {
            let delay = 0;
            if (context.type === 'data' && context.mode === 'default') {
              delay = context.dataIndex * 100;
            }
            return delay;
          }
        },
        plugins: {
          legend: {
            display: false
          },
          tooltip: {
            enabled: true,
            backgroundColor: 'rgba(0, 0, 0, 0.8)',
            titleColor: 'rgba(255, 255, 255, 0.9)',
            bodyColor: 'rgba(255, 255, 255, 0.7)',
            borderColor: 'rgba(255, 255, 255, 0.1)',
            borderWidth: 1,
            padding: 10,
            displayColors: false,
            callbacks: {
              title: (items) => items[0].label,
              label: (item) => `${item.parsed.y} articles`
            }
          }
        },
        scales: {
          x: {
            grid: {
              display: false
            },
            ticks: {
              color: 'rgba(255, 255, 255, 0.25)',
              font: {
                family: 'Syncopate',
                size: 9
              },
              maxRotation: 45,
              minRotation: 45
            },
            border: {
              color: 'rgba(255, 255, 255, 0.05)'
            }
          },
          y: {
            grid: {
              color: 'rgba(255, 255, 255, 0.03)',
              lineWidth: 1
            },
            ticks: {
              color: 'rgba(255, 255, 255, 0.25)',
              font: {
                family: 'Syncopate',
                size: 9
              },
              padding: 10
            },
            border: {
              color: 'rgba(255, 255, 255, 0.05)'
            }
          }
        },
        interaction: {
          intersect: false,
          mode: 'index'
        }
      }
    });

    console.log('Chart created successfully:', this.chart);
  }
}
