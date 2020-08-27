import {Injectable} from '@angular/core';
import {HttpClient, HttpHeaders} from '@angular/common/http';
import {Router} from '@angular/router';

@Injectable()
export class UserService {
 
  // http options used for making API calls
  private httpOptions: any;
 
  // the actual JWT token
  public token: string;
 
  // the token expiration date
  public token_expires: Date;
 
  // the username of the logged in user
  public username: string;
 
  // error messages received from the login attempt
  public errors: any = [];
 
  constructor(private http: HttpClient, private router: Router) {
    this.httpOptions = {
      headers: new HttpHeaders({'Content-Type': 'application/json'})
    };
  }

  private endpoint = "https://smarthydro.central-iot.com/apirest";
  //private endpoint = "http://localhost:8000/apirest"
  //private endpoint = "https://sadistglf.central-iot.com/apirest"

  // Uses http.post() to get an auth token from djangorestframework-jwt endpoint
  public login(user) {

    this.http.post(this.endpoint+'/api-token-auth/', JSON.stringify(user), this.httpOptions).subscribe(
      data => {
        console.log(data);
        this.updateData(data['token']);
        this.router.navigate(['/resumen']);
      },
      err => {
        this.errors = err['error'];
      }
    );
  }
 
  // Refreshes the JWT token, to extend the time the user is logged in
  public refreshToken() {
    this.http.post(this.endpoint+'/api-token-refresh/', JSON.stringify({token: this.token}), this.httpOptions).subscribe(
      data => {
        this.updateData(data['token']);
        this.router.navigate(['/resumen']);
      },
      err => {
        this.errors = err['error'];
      }
    );
  }
 
  public logout() {
    this.token = null;
    this.token_expires = null;
    this.username = null;
  }
 
  private updateData(token) {
    this.token = token;
    this.errors = [];
 
    // decode the token to read the username and expiration timestamp
    const token_parts = this.token.split(/\./);
    const token_decoded = JSON.parse(window.atob(token_parts[1]));
    this.token_expires = new Date(token_decoded.exp * 1000);
    this.username = token_decoded.username;
  }

  public verify_logged_user() {
    if(this.token === undefined) {
        //console.log("Usuario no autenticado");
        //this.router.navigate(['/login']);
        return false;
      }
      else {
        // console.log(this.token);
        return true;
      }
  }
 
}