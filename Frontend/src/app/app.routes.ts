import { Routes } from '@angular/router';
import { DashboardComponent } from './features/dashboard/dashboard.component';
import { ArticlesListComponent } from './features/articles/articles-list.component';
import { SearchComponent } from './features/search/search.component';

export const routes: Routes = [
  { path: '', redirectTo: 'dashboard', pathMatch: 'full' },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'articles', component: ArticlesListComponent },
  { path: 'search', component: SearchComponent }
];
