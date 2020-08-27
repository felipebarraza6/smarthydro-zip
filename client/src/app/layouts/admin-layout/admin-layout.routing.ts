import { Routes } from '@angular/router';

import { DashboardComponent } from '../../dashboard/dashboard.component';
import { UserProfileComponent } from '../../user-profile/user-profile.component';
import { TableListComponent } from '../../table-list/table-list.component';
import { TypographyComponent } from '../../typography/typography.component';
import { IconsComponent } from '../../icons/icons.component';
import { MapsComponent } from '../../maps/maps.component';
import { NotificationsComponent } from '../../notifications/notifications.component';
import { UpgradeComponent } from '../../upgrade/upgrade.component';
import { LoginComponent } from '../../login/login.component';
import { UserSummaryComponent } from '../../user-summary/user-summary.component'; 
import { SensorComponent } from '../../sensor/sensor.component';
import { AuthGuardService } from '../../auth-guard.service';

export const AdminLayoutRoutes: Routes = [

    { path: 'dashboard',      component: DashboardComponent, canActivate: [AuthGuardService]},
    { path: 'resumen',      component: UserSummaryComponent, canActivate: [AuthGuardService]},
    //{ path: 'user-profile',   component: UserProfileComponent, canActivate: [AuthGuardService] },
    //{ path: 'table-list',     component: TableListComponent, canActivate: [AuthGuardService] },
    //{ path: 'typography',     component: TypographyComponent, canActivate: [AuthGuardService] },
    //{ path: 'icons',          component: IconsComponent },
    //{ path: 'maps',           component: MapsComponent },
    { path: 'alertas',  component: NotificationsComponent, canActivate: [AuthGuardService] },
    //{ path: 'upgrade',        component: UpgradeComponent, canActivate: [AuthGuardService] },
    { path: 'login',        component: LoginComponent},
    { path: 'sensor/:id',        component: SensorComponent, canActivate: [AuthGuardService] },
    { path: 'sensor',        component: DashboardComponent, canActivate: [AuthGuardService] },
];
