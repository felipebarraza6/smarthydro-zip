import { Component, OnInit } from '@angular/core';
import { ApiService } from '../api.service';
import { UserService } from '../user.service';
import {Router} from '@angular/router';
import { ActivatedRoute } from '@angular/router';
import * as Chartist from 'chartist';

declare var $: any;

@Component({
	selector: 'app-sensor',
	templateUrl: './sensor.component.html',
	styleUrls: ['./sensor.component.scss']
})
export class SensorComponent implements OnInit {
	uuid: string;
	private sub: any;

	// CONFIGURACION DE CARGA DE DATOS
	loading: boolean = false;
	hasData: boolean = false;

	showNotification(from, align){
		const type = ['','info','success','warning','danger'];

		const color = Math.floor((Math.random() * 4) + 1);

		$.notify({
				icon: "notifications",
				message: "Mensaje Recibido"

		},{
			type: type[color],
			timer: 200,
			placement: {
					from: from,
					align: align
			},
			template: '<div data-notify="container" class="col-xl-2 col-lg-2 col-11 col-sm-4 col-md-3 alert alert-{0} alert-with-icon" role="alert">' +
				'<button mat-button  type="button" aria-hidden="true" class="close mat-button" data-notify="dismiss">  <i class="material-icons">close</i></button>' +
				'<i class="material-icons" data-notify="icon">notifications</i> ' +
				'<span data-notify="title">{1}</span> ' +
				'<span data-notify="message">{2}</span>' +
				'<div class="progress" data-notify="progressbar">' +
					'<div class="progress-bar progress-bar-{0}" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width: 0%;"></div>' +
				'</div>' +
				'<a href="{3}" target="{2}" data-notify="url"></a>' +
			'</div>'
		});
	}

  downloading = false;
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

	getSensorData(): void {
    this.apiService.getData(this.uuid).subscribe(response => {
      console.log(response);
      this.loading = false;
      this.hasData = true;
      this.data = response;
      this.updateChartData();
      this.createCharts();
    })
    this.loading = true;
    //this.hasData = true;
    this.setsocket();
  }

  // DATOS PARA LA CONFIGURACION DE TARJETAS
  data: any;
  getData(): void {
    this.apiService.testBackend().subscribe(response => {
      console.log(response);
    });
  };

  //  VARIABLES PARA GRAFICO DE ULTIMA HORA
  dataUltimaHoraChart: any = {
    labels: [],
    series: [],
  };

  dataUltimoDiaChart: any = {
    labels: [],
    series: [],
  };

  dataUltimaSemanaChart: any = {
    labels: [],
    series: [],
  };

  dataUltimoMesChart: any = {
    labels: [],
    series: [],
  };

  optionsUltimaHoraChart: any = {
    lineSmooth: Chartist.Interpolation.cardinal({
        tension: 0
    }),
    // low: 0,
    // high: 50, // creative tim: we recommend you to set the high sa the biggest value + something for a better look
    chartPadding: { top: 0, right: 0, bottom: 0, left: 0},
  };

  updateChartData(): void {
    this.dataUltimaHoraChart.labels = this.data.resumen.resumen_hora.xdata;
    this.dataUltimaHoraChart.series[0] = this.data.resumen.resumen_hora.ydata;
    let mins = this.dataUltimaHoraChart.labels.map( function(obj) {
      return obj.split(':')[1];
    })
    this.dataUltimaHoraChart.labels = mins;

    this.dataUltimoDiaChart.labels = this.data.resumen.resumen_dia.xdata;
    this.dataUltimoDiaChart.series[0] = this.data.resumen.resumen_dia.ydata;
    let hrs = this.dataUltimoDiaChart.labels.map(function(obj){
      return obj.split(':')[0].split('T')[1];
    });
    this.dataUltimoDiaChart.labels = hrs;

    this.dataUltimaSemanaChart.labels = this.data.resumen.resumen_semana.xdata;
    this.dataUltimaSemanaChart.series[0] = this.data.resumen.resumen_semana.ydata;
    this.dataUltimaSemanaChart.labels = this.dataUltimaSemanaChart.labels.map( function(obj) {
      return obj.split('T')[0].split('-')[2];
    });

    this.dataUltimoMesChart.labels = this.data.resumen.resumen_mes.xdata;
    this.dataUltimoMesChart.series[0] = this.data.resumen.resumen_mes.ydata;
    this.dataUltimoMesChart.labels = this.dataUltimoMesChart.labels.map( function(obj) {
      return obj.split('T')[0].split('-')[2];
    });
  };
  createCharts(): void {
    var ultimaHoraChart = new Chartist.Line('#ultimaHoraChart', this.dataUltimaHoraChart, this.optionsUltimaHoraChart);
    var ultimoDiaChart = new Chartist.Line('#ultimoDiaChart', this.dataUltimoDiaChart, this.optionsUltimaHoraChart);
    var ultimaSemanaChart = new Chartist.Line('#ultimaSemanaChart', this.dataUltimaSemanaChart, this.optionsUltimaHoraChart);
    var ultimoMesChart = new Chartist.Line('#ultimoMesChart', this.dataUltimoMesChart, this.optionsUltimaHoraChart);
    //this.startAnimationForLineChart(ultimaHoraChart);
  };

  socket: any;
  // WSURL = 'ws://127.0.0.1:8000/ws/chat/'
  WSURL = 'wss://smarthydro.central-iot.com/ws/chat/';
  last_value: any;
  last_timestamp: any;
  onloadDate: any; 
  datestring: string;  //= Data(onloadDate).
  setsocket() {
    this.socket = new WebSocket(this.WSURL+this.uuid);
    // console.log(this.socket);
    this.socket.onopen = () => {
      console.log("Websockets connection created!");
    }
    // what will happen on message!
    this.socket.onmessage = (event) => {
      // console.log(event);
      this.handleMessage(event);
    }

    if (this.socket.readyState == WebSocket.OPEN) {
      this.socket.onopen(null);
    }
  }

  handleMessage(message) {
    console.log(message);
    let data = JSON.parse(message.data);
    let msg = JSON.parse(data.message);
    console.log(msg);
    this.data.resumen.ultimo.valor = msg.lectura.valor;
    this.data.resumen.ultimo.datetime = msg.lectura.medido;
    this.showNotification('top','left');
  }

  constructor(private apiService: ApiService, private _userService: UserService, private router: Router, private route: ActivatedRoute) { }

	ngOnInit() {
		if(this._userService.token === undefined) {
			console.log("Usuario no autenticado");
			this.router.navigate(['/login']);
		}
		else {
			console.log(this._userService.token);
			this.sub = this.route.params.subscribe(params => {
				this.uuid = params['id']; // (+) converts string 'id' to a number
				console.log(this.uuid);
			});
			this.getSensorData()

			// this.get_user_data();
			//this.apiService.get_user_data().subscribe(response => {
			//	console.log(response);
			//});
		}
	}

	ngOnDestroy(): void {
		this.socket.close();
	}

}
