(window.webpackJsonp=window.webpackJsonp||[]).push([[101,37,86,157],{782:function(e,n,t){"use strict";t.r(n);var o={props:{url:{type:String},icon:{type:String},iconColor:{type:String,default:function(){return"white"}},tooltip:{type:String},showBadge:{type:Boolean,default:!1},badgeVerticalPosition:{type:String},badgeHorizontalPosition:{type:String},badgeBorderColor:{type:String}},methods:{onClickIcon:function(){this.$emit("click-icon")}}},r=t(31),component=Object(r.a)(o,(function(){var e=this,n=e._self._c;return n("BaseButton",{staticClass:"icon-with-badge",attrs:{"data-title":e.tooltip},on:{"on-click":e.onClickIcon}},[n("i",{directives:[{name:"badge",rawName:"v-badge",value:{showBadge:e.showBadge,verticalPosition:e.badgeVerticalPosition,horizontalPosition:e.badgeHorizontalPosition,borderColor:e.badgeBorderColor},expression:"{\n      showBadge: showBadge,\n      verticalPosition: badgeVerticalPosition,\n      horizontalPosition: badgeHorizontalPosition,\n      borderColor: badgeBorderColor,\n    }"}],key:e.showBadge,staticClass:"icon-wrapper"},[n("svgicon",{attrs:{name:e.icon,width:"22",height:"22",color:e.iconColor}})],1)])}),[],!1,null,null,null);n.default=component.exports;installComponents(component,{BaseButton:t(460).default})},797:function(e,n,t){"use strict";t.r(n);t(841);var o={name:"QuestionHeader",props:{title:{type:String,required:!0},tooltipMessage:{type:String,default:function(){return""}},isRequired:{type:Boolean,default:function(){return!1}}},computed:{showIcon:function(){var e;return!(null===(e=this.tooltipMessage)||void 0===e||!e.length)}}},r=(t(963),t(31)),component=Object(r.a)(o,(function(){var e=this,n=e._self._c;return n("div",{staticClass:"title-area --body1"},[n("span",{directives:[{name:"optional-field",rawName:"v-optional-field",value:!e.isRequired,expression:"!isRequired"}],domProps:{textContent:e._s(e.title)}}),e._v(" "),e.showIcon?n("BaseIconWithBadge",{directives:[{name:"tooltip",rawName:"v-tooltip",value:{content:e.tooltipMessage,backgroundColor:"#FFF"},expression:"{ content: tooltipMessage, backgroundColor: '#FFF' }"}],staticClass:"icon-info",attrs:{icon:"info",id:"".concat(e.title,"QuestionHeader"),"show-badge":!1,iconColor:"#acacac","badge-vertical-position":"top","badge-horizontal-position":"right","badge-border-color":"white"}}):e._e()],1)}),[],!1,null,"59e505b8",null);n.default=component.exports;installComponents(component,{BaseIconWithBadge:t(782).default})},841:function(e,n,t){t(174).register({info:{width:41,height:40,viewBox:"0 0 41 40",data:'<path pid="0" d="M19 18.47a1.5 1.5 0 113 0v9a1.5 1.5 0 01-3 0v-9zM20.5 11.077a1.5 1.5 0 100 3 1.5 1.5 0 000-3z" _fill="#000"/><path pid="1" fill-rule="evenodd" clip-rule="evenodd" d="M20.5 5c-8.284 0-15 6.716-15 15 0 8.284 6.716 15 15 15 8.284 0 15-6.716 15-15 0-8.284-6.716-15-15-15zm-12 15c0 6.627 5.373 12 12 12s12-5.373 12-12-5.373-12-12-12-12 5.373-12 12z" _fill="#000"/>'}})},852:function(e,n,t){var content=t(964);content.__esModule&&(content=content.default),"string"==typeof content&&(content=[[e.i,content,""]]),content.locals&&(e.exports=content.locals);(0,t(81).default)("3dc40e36",content,!0,{sourceMap:!1})},963:function(e,n,t){"use strict";t(852)},964:function(e,n,t){var o=t(80),r=t(94),c=t(95),l=t(96),d=o((function(i){return i[1]})),h=r(c),f=r(l);d.push([e.i,'/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */@font-face{font-family:"raptor_v2_premiumbold";font-style:normal;font-weight:400;src:url('+h+') format("woff2"),url('+f+') format("woff")}/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */.title-area[data-v-59e505b8]{color:rgba(0,0,0,.87);font-weight:500}.icon[data-v-59e505b8]{color:rgba(0,0,0,.37)}.info-icon[data-v-59e505b8]{display:flex;flex-basis:37px}span[data-v-59e505b8]{word-break:break-word}.icon-info[data-v-59e505b8]{display:inline-flex;height:20px;margin:0;overflow:inherit;padding:0;vertical-align:middle;width:20px}.icon-info[data-title][data-v-59e505b8]{overflow:visible;position:relative}.icon-info[data-title][data-v-59e505b8]:after,.icon-info[data-title][data-v-59e505b8]:before{margin-top:0}',""]),d.locals={},e.exports=d}}]);