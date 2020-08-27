import { Injectable } from '@angular/core';
import { Router, CanActivate } from '@angular/router';
import { UserService } from './user.service';

@Injectable()
export class AuthGuardService implements CanActivate {

  constructor(private _userService: UserService, public router: Router) {}

  canActivate(): boolean {
    if (!this._userService.verify_logged_user()) {
      this.router.navigate(['login']);
      return false;
    }
    return true;
  }

}