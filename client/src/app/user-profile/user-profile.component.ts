import { Component, OnInit } from '@angular/core';
import {Router} from '@angular/router';
import { UserService } from '../user.service';

@Component({
  selector: 'app-user-profile',
  templateUrl: './user-profile.component.html',
  styleUrls: ['./user-profile.component.css']
})
export class UserProfileComponent implements OnInit {

  constructor(private _userService: UserService, private router: Router) { }

  ngOnInit() {
  	if(this._userService.token === undefined) {
      console.log("Usuario no autenticado");
      this.router.navigate(['/login']);
    }
    else {
      console.log(this._userService.token);
    }
  }

}
