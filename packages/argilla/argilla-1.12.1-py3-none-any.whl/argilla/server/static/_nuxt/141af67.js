(window.webpackJsonp=window.webpackJsonp||[]).push([[57,58],{780:function(e,t,n){var content=n(813);content.__esModule&&(content=content.default),"string"==typeof content&&(content=[[e.i,content,""]]),content.locals&&(e.exports=content.locals);(0,n(81).default)("39e7b008",content,!0,{sourceMap:!1})},783:function(e,t,n){"use strict";n.r(t);n(114),n(115),n(462);var o={model:{prop:"areChecked",event:"change"},props:["areChecked","value","id","disabled","label","allowMultiple"],data:function(){return{checked:this.value||!1}},computed:{classes:function(){return{active:Array.isArray(this.areChecked)?this.areChecked.includes(this.value):this.checked,disabled:this.disabled}}},watch:{value:function(){this.checked=!!this.value}},methods:{toggleCheck:function(){if(!this.disabled){var e=this.areChecked,t=e.indexOf(this.value);t>=0?e.splice(t,1):(e.length&&!this.allowMultiple&&(e=[]),e.push(this.value)),this.$emit("change",e)}}}},r=(n(812),n(31)),component=Object(r.a)(o,(function(){var e=this,t=e._self._c;return t("div",{staticClass:"annotation-button",class:[e.classes,e.allowMultiple?"multiple":"single"]},[t("label",{staticClass:"button",attrs:{for:e.id},on:{click:function(t){return t.preventDefault(),e.toggleCheck.apply(null,arguments)}}},[t("span",{staticClass:"annotation-button-data__text",attrs:{title:e.label.class}},[e._v(e._s(e.label.class)+"\n    ")]),e._v(" "),e.label.score>0?t("div",{staticClass:"annotation-button-data__info"},[t("span",[e._v(e._s(e._f("percent")(e.label.score)))])]):e._e()]),e._v(" "),t("div",{staticClass:"annotation-button-container",attrs:{tabindex:"0"},on:{click:function(t){return t.stopPropagation(),e.toggleCheck.apply(null,arguments)}}},[t("input",{attrs:{id:e.id,type:"checkbox",disabled:e.disabled},domProps:{value:e.value,checked:e.checked}})])])}),[],!1,null,"7b6ca38d",null);t.default=component.exports},812:function(e,t,n){"use strict";n(780)},813:function(e,t,n){var o=n(80),r=n(94),c=n(95),l=n(96),d=o((function(i){return i[1]})),h=r(c),f=r(l);d.push([e.i,'/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */@font-face{font-family:"raptor_v2_premiumbold";font-style:normal;font-weight:400;src:url('+h+') format("woff2"),url('+f+') format("woff")}/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */.annotation-button[data-v-7b6ca38d]{display:inline-flex;margin:16px 8px 16px 0;position:relative;width:auto}.annotation-button .annotation-button-container[data-v-7b6ca38d]{display:none}.annotation-button.label-button[data-v-7b6ca38d]{color:#4c4ea3;margin:3.5px;max-width:238px;padding:0;transition:all .3s ease}.annotation-button.label-button .button[data-v-7b6ca38d]{background:#f0f0fe;border-radius:25px;box-shadow:0;color:#4c4ea3;cursor:pointer;display:flex;font-weight:500;height:40px;line-height:40px;outline:none;overflow:hidden;padding-left:16px;padding-right:16px;transition:all .2s ease-in-out;width:100%}.annotation-button.label-button.predicted-label .button[data-v-7b6ca38d]{background:#d6d6ff}.annotation-button.label-button.active[data-v-7b6ca38d]{box-shadow:none;transition:all .2s ease-in-out}.annotation-button.label-button.active .button[data-v-7b6ca38d]{background:#4c4ea3;box-shadow:none;transition:all .2s ease-in-out}.annotation-button.label-button.active:hover .button[data-v-7b6ca38d]{box-shadow:0 0 1px 0 hsla(0,0%,83%,.5),inset 0 -2px 6px 0 #3b3c81;transition:all .2s ease-in-out}.annotation-button.label-button.active[data-v-7b6ca38d]:after{display:none!important}.annotation-button.label-button.active .annotation-button-data__info[data-v-7b6ca38d],.annotation-button.label-button.active .annotation-button-data__score[data-v-7b6ca38d],.annotation-button.label-button.active .annotation-button-data__text[data-v-7b6ca38d]{color:#fff}.annotation-button.label-button .annotation-button-data[data-v-7b6ca38d]{overflow:hidden;transition:transform .3s ease}.annotation-button.label-button .annotation-button-data__text[data-v-7b6ca38d]{display:inline-block;margin:auto;max-width:200px;overflow:hidden;text-overflow:ellipsis;vertical-align:top;white-space:nowrap}.annotation-button.label-button .annotation-button-data__info[data-v-7b6ca38d]{margin-left:1em;margin-right:0;transform:translateY(0);transition:all .3s ease}.annotation-button.label-button .annotation-button-data__score[data-v-7b6ca38d]{border-radius:2px;display:inline-block;font-size:12px;font-size:.75rem;line-height:1.5em;min-width:40px;text-align:center}.annotation-button.label-button.predicted-label:not(.active):hover .button[data-v-7b6ca38d]{background:#ccf}.annotation-button.label-button:not(.active):hover .button[data-v-7b6ca38d]{background:#e6e6fd}.annotation-button.disabled[data-v-7b6ca38d]{opacity:.5}.annotation-button.non-reactive[data-v-7b6ca38d]{cursor:pointer;pointer-events:none}.annotation-button.non-reactive .button[data-v-7b6ca38d]{background:#e0e1ff!important;opacity:.5}.annotation-button.non-reactive .button>*[data-v-7b6ca38d]{color:#4c4ea3!important}.annotation-button[data-v-7b6ca38d]:not(.disabled),.annotation-button:not(.disabled) .annotation-button[data-v-7b6ca38d]{cursor:pointer}.annotation-button .annotation-button[data-v-7b6ca38d]{height:20px;line-height:20px;padding-left:8px}',""]),d.locals={},e.exports=d},814:function(e,t,n){var content=n(889);content.__esModule&&(content=content.default),"string"==typeof content&&(content=[[e.i,content,""]]),content.locals&&(e.exports=content.locals);(0,n(81).default)("a462cf2e",content,!0,{sourceMap:!1})},888:function(e,t,n){"use strict";n(814)},889:function(e,t,n){var o=n(80),r=n(94),c=n(95),l=n(96),d=o((function(i){return i[1]})),h=r(c),f=r(l);d.push([e.i,'/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */@font-face{font-family:"raptor_v2_premiumbold";font-style:normal;font-weight:400;src:url('+h+') format("woff2"),url('+f+') format("woff")}/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */.label-button[data-v-0cea7818]{max-width:238px;min-width:80px}.annotation-area[data-v-0cea7818]{margin-top:32px}.feedback-interactions[data-v-0cea7818]{margin:0 auto;padding-right:0}@media(min-width:1451px){.feedback-interactions[data-v-0cea7818]{margin-left:0;max-width:calc(60% + 200px)}}.feedback-interactions__more[data-v-0cea7818]{display:inline-block;margin:3.5px}',""]),d.locals={},e.exports=d},918:function(e,t,n){"use strict";n.r(t);n(114),n(115),n(57),n(48),n(65),n(66);var o=n(30),r=n(26),c=n(37),l=(n(41),n(236),n(47),n(10),n(50),n(463),n(49),n(35),n(175),n(23)),d=n(237);function h(object,e){var t=Object.keys(object);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(object);e&&(n=n.filter((function(e){return Object.getOwnPropertyDescriptor(object,e).enumerable}))),t.push.apply(t,n)}return t}function f(e){for(var i=1;i<arguments.length;i++){var source=null!=arguments[i]?arguments[i]:{};i%2?h(Object(source),!0).forEach((function(t){Object(r.a)(e,t,source[t])})):Object.getOwnPropertyDescriptors?Object.defineProperties(e,Object.getOwnPropertyDescriptors(source)):h(Object(source)).forEach((function(t){Object.defineProperty(e,t,Object.getOwnPropertyDescriptor(source,t))}))}return e}var L={components:{ClassifierAnnotationButton:n(783).default},mixins:[Object(d.a)({idProp:function(e){return"".concat(e.datasetName,"-").concat(e.record.id)}})],props:{record:{type:Object,required:!0},datasetName:{type:String,required:!0},isMultiLabel:{type:Boolean,default:!1},paginationSize:{type:Number,required:!0},inputLabels:{type:Array,required:!0}},idState:function(){return{searchText:"",selectedLabels:[],shownLabels:this.maxVisibleLabels}},watch:{annotationLabels:function(e,t){e!==t&&(this.selectedLabels=this.appliedLabels)}},computed:{searchText:{get:function(){return this.idState.searchText},set:function(e){this.idState.searchText=e}},selectedLabels:{get:function(){return this.idState.selectedLabels},set:function(e){this.idState.selectedLabels=e}},shownLabels:{get:function(){return this.allowToShowAllLabels?this.labels.length:this.idState.shownLabels},set:function(e){this.idState.shownLabels=e}},maxVisibleLabels:function(){return l.a.MAX_VISIBLE_LABELS},visibleLabels:function(){var e=this.filteredLabels.filter((function(e){return e.selected})).length,t=this.shownLabels<this.filteredLabels.length?this.shownLabels-e:this.shownLabels,n=0;return this.filteredLabels.filter((function(e){return e.selected?e:n<t?(n++,e):void 0}))},filteredLabels:function(){var e=this;return this.labels.filter((function(label){return label.class.toLowerCase().match(e.searchText.toLowerCase())}))},appliedLabels:function(){return this.labels.filter((function(e){return e.selected})).map((function(label){return label.class}))},labels:function(){var e=Object.assign.apply(Object,[{}].concat(Object(c.a)(this.inputLabels.map((function(label){return Object(r.a)({},label,{score:0,selected:!1})})))));return this.annotationLabels.forEach((function(label){e[label.class]={score:0,selected:!0}})),this.predictionLabels.forEach((function(label){var t=e[label.class]||label;e[label.class]=f(f({},t),{},{score:label.score})})),Object.entries(e).map((function(e){var t=Object(o.a)(e,2);return f({class:t[0]},t[1])}))},annotationLabels:function(){var e;return(null===(e=this.record.currentAnnotation)||void 0===e?void 0:e.labels)||[]},predictionLabels:function(){var e;return(null===(e=this.record.prediction)||void 0===e?void 0:e.labels)||[]},allowToShowAllLabels:function(){return 1===this.paginationSize||!1},predictedAs:function(){return this.record.predicted_as}},mounted:function(){this.selectedLabels=this.appliedLabels},methods:{updateLabels:function(e){this.isMultiLabel||e.length>0?this.annotate():this.resetAnnotations()},resetAnnotations:function(){this.$emit("reset",this.record)},annotate:function(){this.isMultiLabel?this.$emit("update-labels",this.selectedLabels):this.$emit("validate",this.selectedLabels)},expandLabels:function(){this.shownLabels=this.filteredLabels.length},collapseLabels:function(){this.shownLabels=this.maxVisibleLabels},onSearchLabel:function(e){this.searchText=e}}},m=(n(888),n(31)),component=Object(m.a)(L,(function(){var e=this,t=e._self._c;return e.labels.length?t("div",{staticClass:"annotation-area"},[e.labels.length>e.maxVisibleLabels?t("label-search",{attrs:{searchText:e.searchText},on:{input:e.onSearchLabel}}):e._e(),e._v(" "),t("div",{staticClass:"feedback-interactions"},[e._l(e.visibleLabels,(function(label){return t("classifier-annotation-button",{key:"".concat(label.class),class:["label-button",e.predictedAs.includes(label.class)?"predicted-label":null],attrs:{id:label.class,"allow-multiple":e.isMultiLabel,label:label,"data-title":label.class,value:label.class},on:{change:e.updateLabels},model:{value:e.selectedLabels,callback:function(t){e.selectedLabels=t},expression:"selectedLabels"}})})),e._v(" "),e.allowToShowAllLabels?e._e():[e.visibleLabels.length<e.filteredLabels.length?t("base-button",{staticClass:"feedback-interactions__more secondary text",on:{click:function(t){return e.expandLabels()}}},[e._v("+"+e._s(e.filteredLabels.length-e.visibleLabels.length))]):e.visibleLabels.length>e.maxVisibleLabels&&!e.allowToShowAllLabels?t("base-button",{staticClass:"feedback-interactions__more secondary text",on:{click:function(t){return e.collapseLabels()}}},[e._v("Show less")]):e._e()]],2)],1):e._e()}),[],!1,null,"0cea7818",null);t.default=component.exports;installComponents(component,{LabelSearch:n(844).default,ClassifierAnnotationButton:n(783).default,BaseButton:n(460).default})}}]);