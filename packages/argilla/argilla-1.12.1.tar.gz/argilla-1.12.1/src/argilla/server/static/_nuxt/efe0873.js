(window.webpackJsonp=window.webpackJsonp||[]).push([[70,73],{1184:function(e,n,o){var content=o(1273);content.__esModule&&(content=content.default),"string"==typeof content&&(content=[[e.i,content,""]]),content.locals&&(e.exports=content.locals);(0,o(81).default)("cac59b3e",content,!0,{sourceMap:!1})},1272:function(e,n,o){"use strict";o(1184)},1273:function(e,n,o){var t=o(80),r=o(94),c=o(95),d=o(96),f=t((function(i){return i[1]})),l=r(c),h=r(d);f.push([e.i,'/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */@font-face{font-family:"raptor_v2_premiumbold";font-style:normal;font-weight:400;src:url('+l+') format("woff2"),url('+h+') format("woff")}/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */.container[data-v-949e2ae0]{margin:0 auto;padding:4em;padding-right:126px;transition:padding .25s linear .2s}@media(min-width:1101px){.--metrics .container[data-v-949e2ae0]{padding-right:375px;transition:padding .25s linear}}.entities__container[data-v-949e2ae0]{-ms-overflow-style:none;scrollbar-width:none}.entities__container[data-v-949e2ae0]::-webkit-scrollbar{display:none}.container[data-v-949e2ae0]{margin-left:0;padding-bottom:0;padding-top:0}.entities__wrapper[data-v-949e2ae0]{position:relative}.entities__container[data-v-949e2ae0]{border-radius:10px;margin-bottom:8px;max-height:189px;overflow:auto}.--annotation .entities__container[data-v-949e2ae0]{margin-bottom:16px}.entities__container__button[data-v-949e2ae0]{display:inline-block}.entity-label[data-v-949e2ae0]{margin:4px}',""]),f.locals={},e.exports=f},1368:function(e,n,o){"use strict";o.r(n);o(74);var t={props:{labels:{type:Array,required:!0}},data:function(){return{showExpandedList:!1,MAX_LABELS_NUMBER:10}},computed:{visibleLabels:function(){var e=this.showExpandedList?this.labels:this.showMaxLabels(this.labels);return e},numberOfLabels:function(){return this.labels.length},isCollapsable:function(){return this.numberOfLabels>this.MAX_LABELS_NUMBER},buttonText:function(){return this.showExpandedList?"Show less":"+ ".concat(this.numberOfLabels-this.MAX_LABELS_NUMBER)}},methods:{toggleLabelsArea:function(){this.showExpandedList=!this.showExpandedList},showMaxLabels:function(e){return e.slice(0,this.MAX_LABELS_NUMBER)}}},r=(o(1272),o(31)),component=Object(r.a)(t,(function(){var e=this,n=e._self._c;return n("div",{staticClass:"container"},[n("div",{staticClass:"entities__wrapper"},[e.numberOfLabels?n("div",{staticClass:"entities__container"},[e._l(e.visibleLabels,(function(label,o){return n("entity-label",{key:o,attrs:{label:label.text,shortcut:label.shortcut,color:"color_".concat(label.color_id%e.$entitiesMaxColors)}})})),e._v(" "),e.isCollapsable?n("base-button",{staticClass:"entities__container__button secondary text",on:{click:e.toggleLabelsArea}},[e._v("\n        "+e._s(e.buttonText)+"\n      ")]):e._e()],2):e._e()])])}),[],!1,null,"949e2ae0",null);n.default=component.exports;installComponents(component,{EntityLabel:o(912).default,BaseButton:o(460).default})},807:function(e,n,o){var content=o(878);content.__esModule&&(content=content.default),"string"==typeof content&&(content=[[e.i,content,""]]),content.locals&&(e.exports=content.locals);(0,o(81).default)("78d8e094",content,!0,{sourceMap:!1})},877:function(e,n,o){"use strict";o(807)},878:function(e,n,o){var t=o(80),r=o(94),c=o(95),d=o(96),f=t((function(i){return i[1]})),l=r(c),h=r(d);f.push([e.i,'/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */@font-face{font-family:"raptor_v2_premiumbold";font-style:normal;font-weight:400;src:url('+l+') format("woff2"),url('+h+') format("woff")}/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */.entity-label[data-v-2ef69a4b]{align-items:center;color:rgba(0,0,0,.87);display:inline-flex;font-size:13px;font-size:.8125rem;font-weight:500;max-height:28px;padding:.3em;position:relative}.entity-label .shortcut[data-v-2ef69a4b]{color:rgba(0,0,0,.6);font-weight:lighter;margin-left:16px}.color_0[data-v-2ef69a4b]{background:#fffcc2}.color_0.--prediction[data-v-2ef69a4b]{background:none;border-bottom:5px solid #fffcc2;padding:.3em 0}.color_1[data-v-2ef69a4b]{background:#c8ffc2}.color_1.--prediction[data-v-2ef69a4b]{background:none;border-bottom:5px solid #c8ffc2;padding:.3em 0}.color_2[data-v-2ef69a4b]{background:#c2fff6}.color_2.--prediction[data-v-2ef69a4b]{background:none;border-bottom:5px solid #c2fff6;padding:.3em 0}.color_3[data-v-2ef69a4b]{background:#c2cdff}.color_3.--prediction[data-v-2ef69a4b]{background:none;border-bottom:5px solid #c2cdff;padding:.3em 0}.color_4[data-v-2ef69a4b]{background:#f1c2ff}.color_4.--prediction[data-v-2ef69a4b]{background:none;border-bottom:5px solid #f1c2ff;padding:.3em 0}.color_5[data-v-2ef69a4b]{background:#ffc2d3}.color_5.--prediction[data-v-2ef69a4b]{background:none;border-bottom:5px solid #ffc2d3;padding:.3em 0}.color_6[data-v-2ef69a4b]{background:#ffebc2}.color_6.--prediction[data-v-2ef69a4b]{background:none;border-bottom:5px solid #ffebc2;padding:.3em 0}.color_7[data-v-2ef69a4b]{background:#d9ffc2}.color_7.--prediction[data-v-2ef69a4b]{background:none;border-bottom:5px solid #d9ffc2;padding:.3em 0}.color_8[data-v-2ef69a4b]{background:#c2ffe5}.color_8.--prediction[data-v-2ef69a4b]{background:none;border-bottom:5px solid #c2ffe5;padding:.3em 0}.color_9[data-v-2ef69a4b]{background:#c2deff}.color_9.--prediction[data-v-2ef69a4b]{background:none;border-bottom:5px solid #c2deff;padding:.3em 0}.color_10[data-v-2ef69a4b]{background:#e0c2ff}.color_10.--prediction[data-v-2ef69a4b]{background:none;border-bottom:5px solid #e0c2ff;padding:.3em 0}.color_11[data-v-2ef69a4b]{background:#ffc2e4}.color_11.--prediction[data-v-2ef69a4b]{background:none;border-bottom:5px solid #ffc2e4;padding:.3em 0}.color_12[data-v-2ef69a4b]{background:#ffdac2}.color_12.--prediction[data-v-2ef69a4b]{background:none;border-bottom:5px solid #ffdac2;padding:.3em 0}.color_13[data-v-2ef69a4b]{background:#eaffc2}.color_13.--prediction[data-v-2ef69a4b]{background:none;border-bottom:5px solid #eaffc2;padding:.3em 0}.color_14[data-v-2ef69a4b]{background:#c2ffd4}.color_14.--prediction[data-v-2ef69a4b]{background:none;border-bottom:5px solid #c2ffd4;padding:.3em 0}.color_15[data-v-2ef69a4b]{background:#c2efff}.color_15.--prediction[data-v-2ef69a4b]{background:none;border-bottom:5px solid #c2efff;padding:.3em 0}.color_16[data-v-2ef69a4b]{background:#cec2ff}.color_16.--prediction[data-v-2ef69a4b]{background:none;border-bottom:5px solid #cec2ff;padding:.3em 0}.color_17[data-v-2ef69a4b]{background:#ffc2f5}.color_17.--prediction[data-v-2ef69a4b]{background:none;border-bottom:5px solid #ffc2f5;padding:.3em 0}.color_18[data-v-2ef69a4b]{background:#ffc9c2}.color_18.--prediction[data-v-2ef69a4b]{background:none;border-bottom:5px solid #ffc9c2;padding:.3em 0}.color_19[data-v-2ef69a4b]{background:#fbffc2}.color_19.--prediction[data-v-2ef69a4b]{background:none;border-bottom:5px solid #fbffc2;padding:.3em 0}.color_20[data-v-2ef69a4b]{background:#c2ffc3}.color_20.--prediction[data-v-2ef69a4b]{background:none;border-bottom:5px solid #c2ffc3;padding:.3em 0}.color_21[data-v-2ef69a4b]{background:#c2fffd}.color_21.--prediction[data-v-2ef69a4b]{background:none;border-bottom:5px solid #c2fffd;padding:.3em 0}.color_22[data-v-2ef69a4b]{background:#c2c6ff}.color_22.--prediction[data-v-2ef69a4b]{background:none;border-bottom:5px solid #c2c6ff;padding:.3em 0}.color_23[data-v-2ef69a4b]{background:#f8c2ff}.color_23.--prediction[data-v-2ef69a4b]{background:none;border-bottom:5px solid #f8c2ff;padding:.3em 0}.color_24[data-v-2ef69a4b]{background:#ffc2cc}.color_24.--prediction[data-v-2ef69a4b]{background:none;border-bottom:5px solid #ffc2cc;padding:.3em 0}.color_25[data-v-2ef69a4b]{background:#fff2c2}.color_25.--prediction[data-v-2ef69a4b]{background:none;border-bottom:5px solid #fff2c2;padding:.3em 0}.color_26[data-v-2ef69a4b]{background:#d2ffc2}.color_26.--prediction[data-v-2ef69a4b]{background:none;border-bottom:5px solid #d2ffc2;padding:.3em 0}.color_27[data-v-2ef69a4b]{background:#c2ffec}.color_27.--prediction[data-v-2ef69a4b]{background:none;border-bottom:5px solid #c2ffec;padding:.3em 0}.color_28[data-v-2ef69a4b]{background:#c2d7ff}.color_28.--prediction[data-v-2ef69a4b]{background:none;border-bottom:5px solid #c2d7ff;padding:.3em 0}.color_29[data-v-2ef69a4b]{background:#e7c2ff}.color_29.--prediction[data-v-2ef69a4b]{background:none;border-bottom:5px solid #e7c2ff;padding:.3em 0}.color_30[data-v-2ef69a4b]{background:#ffc2dd}.color_30.--prediction[data-v-2ef69a4b]{background:none;border-bottom:5px solid #ffc2dd;padding:.3em 0}.color_31[data-v-2ef69a4b]{background:#ffe1c2}.color_31.--prediction[data-v-2ef69a4b]{background:none;border-bottom:5px solid #ffe1c2;padding:.3em 0}.color_32[data-v-2ef69a4b]{background:#e3ffc2}.color_32.--prediction[data-v-2ef69a4b]{background:none;border-bottom:5px solid #e3ffc2;padding:.3em 0}.color_33[data-v-2ef69a4b]{background:#c2ffdb}.color_33.--prediction[data-v-2ef69a4b]{background:none;border-bottom:5px solid #c2ffdb;padding:.3em 0}.color_34[data-v-2ef69a4b]{background:#c2e9ff}.color_34.--prediction[data-v-2ef69a4b]{background:none;border-bottom:5px solid #c2e9ff;padding:.3em 0}.color_35[data-v-2ef69a4b]{background:#d5c2ff}.color_35.--prediction[data-v-2ef69a4b]{background:none;border-bottom:5px solid #d5c2ff;padding:.3em 0}.color_36[data-v-2ef69a4b]{background:#ffc2ee}.color_36.--prediction[data-v-2ef69a4b]{background:none;border-bottom:5px solid #ffc2ee;padding:.3em 0}.color_37[data-v-2ef69a4b]{background:#ffd0c2}.color_37.--prediction[data-v-2ef69a4b]{background:none;border-bottom:5px solid #ffd0c2;padding:.3em 0}.color_38[data-v-2ef69a4b]{background:#f4ffc2}.color_38.--prediction[data-v-2ef69a4b]{background:none;border-bottom:5px solid #f4ffc2;padding:.3em 0}.color_39[data-v-2ef69a4b]{background:#c2ffca}.color_39.--prediction[data-v-2ef69a4b]{background:none;border-bottom:5px solid #c2ffca;padding:.3em 0}.color_40[data-v-2ef69a4b]{background:#c2faff}.color_40.--prediction[data-v-2ef69a4b]{background:none;border-bottom:5px solid #c2faff;padding:.3em 0}.color_41[data-v-2ef69a4b]{background:#c4c2ff}.color_41.--prediction[data-v-2ef69a4b]{background:none;border-bottom:5px solid #c4c2ff;padding:.3em 0}.color_42[data-v-2ef69a4b]{background:#ffc2ff}.color_42.--prediction[data-v-2ef69a4b]{background:none;border-bottom:5px solid #ffc2ff;padding:.3em 0}.color_43[data-v-2ef69a4b]{background:#ffc2c5}.color_43.--prediction[data-v-2ef69a4b]{background:none;border-bottom:5px solid #ffc2c5;padding:.3em 0}.color_44[data-v-2ef69a4b]{background:#fff9c2}.color_44.--prediction[data-v-2ef69a4b]{background:none;border-bottom:5px solid #fff9c2;padding:.3em 0}.color_45[data-v-2ef69a4b]{background:#cbffc2}.color_45.--prediction[data-v-2ef69a4b]{background:none;border-bottom:5px solid #cbffc2;padding:.3em 0}.color_46[data-v-2ef69a4b]{background:#c2fff3}.color_46.--prediction[data-v-2ef69a4b]{background:none;border-bottom:5px solid #c2fff3;padding:.3em 0}.color_47[data-v-2ef69a4b]{background:#c2d0ff}.color_47.--prediction[data-v-2ef69a4b]{background:none;border-bottom:5px solid #c2d0ff;padding:.3em 0}.color_48[data-v-2ef69a4b]{background:#edc2ff}.color_48.--prediction[data-v-2ef69a4b]{background:none;border-bottom:5px solid #edc2ff;padding:.3em 0}.color_49[data-v-2ef69a4b]{background:#ffc2d6}.color_49.--prediction[data-v-2ef69a4b]{background:none;border-bottom:5px solid #ffc2d6;padding:.3em 0}',""]),f.locals={},e.exports=f},912:function(e,n,o){"use strict";o.r(n);var t={props:{color:{type:String,required:!0},label:{type:String,required:!0},shortcut:{type:String,default:void 0},isPrediction:{type:Boolean,default:!1}}},r=(o(877),o(31)),component=Object(r.a)(t,(function(){var e=this,n=e._self._c;return n("span",{class:["entity-label",e.color,e.isPrediction?"--prediction":null]},[e._v(e._s(e.label)+"\n  "),e.shortcut?n("span",{staticClass:"shortcut"},[e._v("["+e._s(e.shortcut)+"]")]):e._e()])}),[],!1,null,"2ef69a4b",null);n.default=component.exports}}]);