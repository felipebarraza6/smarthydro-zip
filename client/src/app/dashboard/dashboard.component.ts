import { Component, OnInit } from '@angular/core';
import * as Chartist from 'chartist';
import { ApiService } from '../api.service';
import { UserService } from '../user.service';
import {Router} from '@angular/router';

declare var $: any;

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  // constructor(private heroService: HeroService) { }
  constructor(private apiService: ApiService, private _userService: UserService, private router: Router) { }

  // CONFIGURACION DE CARGA DE DATOS
  loading: boolean = false;
  hasData: boolean = false;
  
  uuidForm = {
    uuid: ''
  }

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

  getSensorData(): void {
    this.apiService.getData(this.uuidForm.uuid).subscribe(response => {
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

    this.dataUltimoDiaChart.labels = this.data.resumen.resumen_dia.xdata;
    this.dataUltimoDiaChart.series[0] = this.data.resumen.resumen_dia.ydata;

    this.dataUltimaSemanaChart.labels = this.data.resumen.resumen_semana.xdata;
    this.dataUltimaSemanaChart.series[0] = this.data.resumen.resumen_semana.ydata;

    this.dataUltimoMesChart.labels = this.data.resumen.resumen_mes.xdata;
    this.dataUltimoMesChart.series[0] = this.data.resumen.resumen_mes.ydata;
  };
  createCharts(): void {
    var ultimaHoraChart = new Chartist.Line('#ultimaHoraChart', this.dataUltimaHoraChart, this.optionsUltimaHoraChart);
    var ultimoDiaChart = new Chartist.Line('#ultimoDiaChart', this.dataUltimoDiaChart, this.optionsUltimaHoraChart);
    var ultimaSemanaChart = new Chartist.Line('#ultimaSemanaChart', this.dataUltimaSemanaChart, this.optionsUltimaHoraChart);
    var ultimoMesChart = new Chartist.Line('#ultimoMesChart', this.dataUltimoMesChart, this.optionsUltimaHoraChart);
    //this.startAnimationForLineChart(ultimaHoraChart);
  };

  socket: any;
  WSURL = 'ws://127.0.0.1:8000/ws/chat/'
  last_value: any;
  last_timestamp: any;
  onloadDate: any; 
  datestring: string;  //= Data(onloadDate).
  setsocket() {
    this.socket = new WebSocket(this.WSURL+this.uuidForm.uuid);
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

  ngOnInit() {
      if(this._userService.token === undefined) {
        console.log("Usuario no autenticado");
        this.router.navigate(['/login']);
      }
      else {
        console.log(this._userService.token);
      }
      this.onloadDate = Date.now();
      this.datestring = this.onloadDate.toString();
  }

}
