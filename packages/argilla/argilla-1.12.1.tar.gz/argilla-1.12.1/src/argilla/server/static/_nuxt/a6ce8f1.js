(window.webpackJsonp=window.webpackJsonp||[]).push([[32],{992:function(t,e,n){"use strict";n.r(e);var o={props:{date:{type:String},format:{type:String}},computed:{timeDifference:function(){return(new Date).getTimezoneOffset()},formattedDate:function(){return"date-relative-now"===this.format?this.$moment(this.date).locale("utc").subtract(this.timeDifference,"minutes").from(Date.now()):this.$moment(this.date).locale("utc").format("YYYY-MM-DD HH:mm")}}},r=n(31),component=Object(r.a)(o,(function(){var t=this;return(0,t._self._c)("span",[t._v(" "+t._s(t.formattedDate)+" ")])}),[],!1,null,null,null);e.default=component.exports}}]);