import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable, of } from 'rxjs';
import {UserService} from './user.service';
import { getFileNameFromResponseContentDisposition, saveFile } from './file-download-helper';
import { RequestOptions, ResponseContentType } from '@angular/http';


@Injectable({
  providedIn: 'root'
})

export class ApiService {
	API_URL = 'http://localhost:8000/apirest/';
	//API_URL = 'https://smarthydro.central-iot.com/apirest/'
	// the user projects
  public user_projects: any;
	
	get_user_data(): any {
		let userUrl = this.API_URL+'resumen-usuario/';
		let httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        'Authorization': 'JWT ' + this._userService.token
      })
    };

		return this.http.get(userUrl, httpOptions);

	};

	getData(sensorUUID): any {
		let resumenUrl = this.API_URL+'resumen-sensor/'+sensorUUID
		let httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        'Authorization': 'JWT ' + this._userService.token
      })
    };

		return this.http.get(resumenUrl, httpOptions);
	};

	downloadSensorData(uuid): any {
		let downloadUrl = this.API_URL+'download-sensor/'+uuid;
		let httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'text/csv',
        //'responseType': 'text',
        //'Response-Type': 'text',  // No alega el compilador pero se equivoca al intentar parsear
        'Authorization': 'JWT ' + this._userService.token
      }),
      responseType: 'text' // Funciono (al menos mostro los resultados sin error de parseo)
    };
    return this.http.get(downloadUrl, {headers: httpOptions.headers, responseType: 'text'});
	}


	testBackend(): any {
		return this.http.get('https://www.sadistglf.com/testing');

	}

  getAlerts(): any {
    let alertsUrl = this.API_URL + 'alertas/';
    let httpOptions = {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        'Authorization': 'JWT ' + this._userService.token
      })
    };
    return this.http.get(alertsUrl, httpOptions);
  }

  constructor( private http: HttpClient, private _userService: UserService) { }
}

