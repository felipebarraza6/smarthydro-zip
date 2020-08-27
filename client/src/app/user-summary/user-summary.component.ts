import { Component, OnInit } from '@angular/core';
import { ApiService } from '../api.service';
import { UserService } from '../user.service';
import {Router} from '@angular/router';
// import { getFileNameFromResponseContentDisposition, saveFile } from '../file-download-helper';

@Component({
  selector: 'app-user-summary',
  templateUrl: './user-summary.component.html',
  styleUrls: ['./user-summary.component.scss']
})
export class UserSummaryComponent implements OnInit {

	projects: any;
	sensors: any;
	deltas = [];
	loading = false;
  downloading = false;
	get_user_data(): any {
		this.loading = true;
		this.apiService.get_user_data().subscribe(response => {
			console.log(response);
			this.loading = false;
			this.projects = response.proyecto;
			this.sensors = response.sensor;
			for(let i = 0; i<this.sensors.length; i++){
				let d1 = new Date();
				let d2 = new Date(this.sensors[i].last_received_ts);
				let delta = (d1.getTime()-d2.getTime())/1000;
				if(delta > 86400){
					this.deltas.push({'unit': 'días', 'value': delta/86400});
				}
				else if(delta > 3600){
					this.deltas.push({'unit': 'horas', 'value': delta/3600});	
				}
				else if(delta > 60){
					this.deltas.push({'unit': 'minutos', 'value': delta/60});	
				}
				else {
					this.deltas.push({'unit': 'segundos', 'value': delta});	
				}
				this.deltas.push();
			}
		});

	}

	download(uuid): any {
		console.log("deberia descargar el archivo!");
		console.log(uuid)
	}

	downloadSensorData(uuid): void {
    /**
    *  used to get file from server
    */
    this.downloading = true;
    this.apiService.downloadSensorData(uuid).subscribe(response => {
    	console.log(response);
    	this.downLoadFile(response, "text/csv");
      this.downloading = false;
    });
    
    //this.http.get(`${environment.apiUrl}`,{responseType: 'arraybuffer',headers:headers})
  }
  /**
   * Method is use to download file.
   * @param data - Array Buffer data
   * @param type - type of the document.
   */
  downLoadFile(data: any, type: string) {

    var blob = new Blob([data], { type: type});
    var url = window.URL.createObjectURL(blob);
    var pwa = window.open(url);
    if (!pwa || pwa.closed || typeof pwa.closed == 'undefined') {
        alert( 'Please disable your Pop-up blocker and try again.');
    }
  }

  constructor(private apiService: ApiService, private _userService: UserService, private router: Router) { }

  ngOnInit() {

  	if(this._userService.token === undefined) {
        console.log("Usuario no autenticado");
        this.router.navigate(['/login']);
      }
      else {
        //console.log(this._userService.token);
        console.log("usuario identificado");
        this.get_user_data();
        //this.apiService.get_user_data().subscribe(response => {
        //	console.log(response);
        //});
      }
  }

}
