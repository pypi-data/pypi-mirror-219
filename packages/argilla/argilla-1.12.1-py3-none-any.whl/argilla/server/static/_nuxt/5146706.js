(window.webpackJsonp=window.webpackJsonp||[]).push([[162,43,144],{1090:function(e,t,n){"use strict";n(982)},1091:function(e,t,n){var r=n(80),o=n(94),c=n(95),l=n(96),d=r((function(i){return i[1]})),h=o(c),f=o(l);d.push([e.i,'/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */@font-face{font-family:"raptor_v2_premiumbold";font-style:normal;font-weight:400;src:url('+h+') format("woff2"),url('+f+') format("woff")}/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */.scroll[data-v-d5cc0928]{-ms-overflow-style:none;scrollbar-width:none}.scroll[data-v-d5cc0928]::-webkit-scrollbar{display:none}.scroll[data-v-d5cc0928]{margin-right:-1em;max-height:calc(100vh - 270px);overflow:auto;padding-right:1em}.metrics__numbers[data-v-d5cc0928]{font-size:18px;font-size:1.125rem;margin-bottom:24px;margin-top:24px}.metrics__numbers span[data-v-d5cc0928]{font-size:40px;font-size:2.5rem;font-weight:700}.color-bullet[data-v-d5cc0928]{border-radius:50%;display:inline-block;height:10px;margin:.3em .3em .3em 0;width:10px}.color-bullet.validated[data-v-d5cc0928]{background:#4c4ea3}.color-bullet.discarded[data-v-d5cc0928]{background:#a1a2cc}',""]),d.locals={},e.exports=d},1115:function(e,t,n){"use strict";n.r(t);n(461),n(10),n(56);var r=n(145),o={props:{dataset:{type:Object,required:!0}},computed:{annotationsSum:function(){return this.dataset.results.aggregations.status.Validated},annotationsProgress:function(){return r.a.find(this.dataset.name)},totalValidated:function(){return this.annotationsProgress.validated},totalDiscarded:function(){return this.annotationsProgress.discarded},totalAnnotated:function(){return this.totalValidated+this.totalDiscarded},total:function(){return this.annotationsProgress.total},datasetName:function(){return this.dataset.name},progress:function(){return((this.totalValidated||0)+(this.totalDiscarded||0))/this.total}}},c=(n(1090),n(31)),component=Object(c.a)(o,(function(){var e=this,t=e._self._c;return e.annotationsProgress?t("div",[t("p",{staticClass:"metrics__title"},[e._v("Progress")]),e._v(" "),t("div",{staticClass:"metrics__info"},[t("p",{staticClass:"metrics__info__name"},[e._v("Total")]),e._v(" "),t("span",{staticClass:"metrics__info__counter"},[e._v(e._s(e._f("percent")(e.progress)))])]),e._v(" "),t("div",{staticClass:"metrics__numbers"},[t("span",[e._v(e._s(e._f("formatNumber")(e.totalAnnotated)))]),e._v("/"+e._s(e._f("formatNumber")(e.total))+"\n  ")]),e._v(" "),t("base-progress",{attrs:{"re-mode":"determinate",multiple:!0,progress:100*e.totalValidated/e.total,"progress-secondary":100*e.totalDiscarded/e.total}}),e._v(" "),t("div",{staticClass:"scroll"},[t("ul",{staticClass:"metrics__list"},[t("li",[t("span",{staticClass:"color-bullet validated"}),e._v(" "),t("label",{staticClass:"metrics__list__name"},[e._v("Validated")]),e._v(" "),t("span",{staticClass:"metrics__list__counter"},[e._v("\n          "+e._s(e._f("formatNumber")(e.totalValidated))+"\n        ")])]),e._v(" "),t("li",[t("span",{staticClass:"color-bullet discarded"}),e._v(" "),t("label",{staticClass:"metrics__list__name"},[e._v("Discarded")]),e._v(" "),t("span",{staticClass:"metrics__list__counter"},[e._v("\n          "+e._s(e._f("formatNumber")(e.totalDiscarded))+"\n        ")])])]),e._v(" "),e._t("default")],2)],1):e._e()}),[],!1,null,"d5cc0928",null);t.default=component.exports;installComponents(component,{BaseProgress:n(845).default})},1493:function(e,t,n){"use strict";n.r(t);n(461),n(10),n(56);var r=n(145),o={props:{dataset:{type:Object,required:!0}},computed:{getInfo:function(){return this.annotationsProgress.annotatedAs},annotationsProgress:function(){return r.a.find(this.dataset.name)}}},c=n(31),component=Object(c.a)(o,(function(){var e=this,t=e._self._c;return t("sidebar-progress",{attrs:{dataset:e.dataset}},[e.annotationsProgress?t("ul",{staticClass:"metrics__list"},e._l(e.getInfo,(function(n,label){return t("li",{key:label},[n>0?[t("label",{staticClass:"metrics__list__name"},[e._v(e._s(label))]),e._v(" "),t("span",{staticClass:"metrics__list__counter"},[e._v(e._s(e._f("formatNumber")(n)))])]:e._e()],2)})),0):e._e()])}),[],!1,null,"6a9842f0",null);t.default=component.exports;installComponents(component,{SidebarProgress:n(1115).default})},790:function(e,t,n){var content=n(840);content.__esModule&&(content=content.default),"string"==typeof content&&(content=[[e.i,content,""]]),content.locals&&(e.exports=content.locals);(0,n(81).default)("58460a70",content,!0,{sourceMap:!1})},839:function(e,t,n){"use strict";n(790)},840:function(e,t,n){var r=n(80),o=n(94),c=n(95),l=n(96),d=r((function(i){return i[1]})),h=o(c),f=o(l);d.push([e.i,'/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */@font-face{font-family:"raptor_v2_premiumbold";font-style:normal;font-weight:400;src:url('+h+') format("woff2"),url('+f+') format("woff")}/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */.progress[data-v-8074c452],.progress--minimal[data-v-8074c452],.progress--multiple[data-v-8074c452]{background:#a1a2cc;border-bottom-right-radius:10px;border-top-left-radius:0;border-top-right-radius:10px;height:22px;margin:0 0 1.5em;overflow:hidden;position:relative}.progress--minimal[data-v-8074c452]:before,.progress--multiple[data-v-8074c452]:before,.progress[data-v-8074c452]:before{background:#fff;bottom:0;content:"";left:0;opacity:.8;position:absolute;right:0;top:0}.progress__container[data-v-8074c452]{position:relative}.progress__container:hover .progress__tooltip[data-v-8074c452]{-webkit-clip-path:none;clip-path:none;opacity:1;transition:opacity .5s linear .3s}.progress__tooltip[data-v-8074c452]{background:#4c4ea3;border-color:lime!important;border:none;border-radius:5px;-webkit-clip-path:circle(0);clip-path:circle(0);color:#fff;font-size:13px;font-size:.8125rem;font-weight:500;margin:0 0 0 6px;opacity:0;padding:.5em 1em;position:absolute;top:-5px;transform:none;transition:opacity .5s linear .3s;z-index:1}.progress__tooltip .triangle[data-v-8074c452]{border-color:transparent #4c4ea3 transparent transparent;border-style:solid;border-width:6px 6px 6px 0;content:"";display:block;height:0;left:-6px;position:absolute;top:calc(50% - 6px);width:0}.progress--minimal[data-v-8074c452]{height:2px}.progress--minimal .progress-track[data-v-8074c452],.progress--minimal .progress-track--secondary[data-v-8074c452]{background:#686a6d}.progress--multiple[data-v-8074c452]{height:20px}.progress-track[data-v-8074c452],.progress-track--secondary[data-v-8074c452]{background:#4c4ea3;border-bottom-left-radius:2px;border-top-left-radius:2px;bottom:0;left:0;position:absolute;top:0;transition:width 1s linear,left 1s linear}.progress-track--secondary[data-v-8074c452]:last-of-type,.progress-track[data-v-8074c452]:last-of-type{border-bottom-left-radius:0;border-top-left-radius:0}.progress-enter-active .progress-track[data-v-8074c452],.progress-enter-active .progress-track--secondary[data-v-8074c452]{animation:progress-8074c452 1s .5s;animation-fill-mode:backwards;transform-origin:0 50%}.progress-track--secondary[data-v-8074c452]{background:#a1a2cc;left:auto;right:0;transition:width 1s linear,left 1s linear}.progress-enter-active .progress-track--secondary[data-v-8074c452]{animation:progress-8074c452 1s 1.5s;animation-fill-mode:backwards}@keyframes progress-8074c452{0%{transform:scaleX(0)}to{transform:scaleX(1)}}',""]),d.locals={},e.exports=d},845:function(e,t,n){"use strict";n.r(t);n(236);var r={props:{progress:{type:Number,default:0},progressSecondary:{type:Number,default:0},multiple:{default:!1,type:Boolean},color:{type:String,default:"#4c4ea3"},colorSecondary:{type:String,default:"#a1a2cc"},tooltip:{default:void 0,type:String}},computed:{styles:function(){return{width:"".concat(this.progress,"%"),backgroundColor:this.color}},backgroundStyles:function(){return{backgroundColor:this.color}},tooltipStyles:function(){return{left:this.progress>80?"70%":"".concat(this.progress,"%"),backgroundColor:this.color}},tooltipTriangleStyles:function(){return{borderRightColor:this.color}},stylesSecondary:function(){return{left:"".concat(this.progress,"%"),width:"".concat(this.progressSecondary,"%"),backgroundColor:this.colorSecondary}}}},o=(n(839),n(31)),component=Object(o.a)(r,(function(){var e=this,t=e._self._c;return t("transition",{attrs:{name:"progress",duration:2500,appear:""}},[t("div",{staticClass:"progress__container"},[e.tooltip?t("p",{staticClass:"progress__tooltip",style:e.tooltipStyles},[t("span",{staticClass:"triangle",style:e.tooltipTriangleStyles}),e._v(e._s(e.tooltip)+"\n    ")]):e._e(),e._v(" "),t("div",{staticClass:"progress",style:e.backgroundStyles},[t("div",{staticClass:"progress-track",style:e.styles}),e._v(" "),e.multiple?t("div",{staticClass:"progress-track--secondary",style:e.stylesSecondary}):e._e()])])])}),[],!1,null,"8074c452",null);t.default=component.exports},982:function(e,t,n){var content=n(1091);content.__esModule&&(content=content.default),"string"==typeof content&&(content=[[e.i,content,""]]),content.locals&&(e.exports=content.locals);(0,n(81).default)("3742ffec",content,!0,{sourceMap:!1})}}]);