(window.webpackJsonp=window.webpackJsonp||[]).push([[29],{1048:function(e,n,t){var content=t(1164);content.__esModule&&(content=content.default),"string"==typeof content&&(content=[[e.i,content,""]]),content.locals&&(e.exports=content.locals);(0,t(81).default)("139886e2",content,!0,{sourceMap:!1})},1163:function(e,n,t){"use strict";t(1048)},1164:function(e,n,t){var r=t(80),o=t(94),c=t(95),d=t(96),l=r((function(i){return i[1]})),h=o(c),f=o(d);l.push([e.i,'/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */@font-face{font-family:"raptor_v2_premiumbold";font-style:normal;font-weight:400;src:url('+h+') format("woff2"),url('+f+') format("woff")}/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */.card{align-items:flex-end;border:1px solid rgba(0,0,0,.1);border-radius:5px;display:flex;padding:16px}.card__buttons{margin-left:auto}.card__title{margin-top:0}.card__text{color:rgba(0,0,0,.37);margin-bottom:0}',""]),l.locals={},e.exports=l},1200:function(e,n,t){"use strict";t.r(n);t(114);var r={props:{title:{type:String},subtitle:{type:String},text:{type:String},buttonText:{type:String},cardType:{type:String,default:"default",validator:function(e){return["danger","warm","info","default"].includes(e)}}},computed:{cardClasses:function(){return{"--danger":"danger"===this.cardType,"--warm":"warm"===this.cardType,"--info":"info"===this.cardType,"--default":"default"===this.cardType}}},methods:{action:function(){this.$emit("card-action")}}},o=(t(1163),t(31)),component=Object(o.a)(r,(function(){var e=this,n=e._self._c;return n("div",{staticClass:"card",class:[e.cardClasses]},[n("div",{staticClass:"card__content"},[e.title?n("h3",{staticClass:"--body1 --light card__title",domProps:{innerHTML:e._s(e.title)}}):e._e(),e._v(" "),e.subtitle?n("h4",{staticClass:"--body2 --semibold card__subtitle"},[e._v("\n      "+e._s(e.subtitle)+"\n    ")]):e._e(),e._v(" "),e.text?n("p",{staticClass:"--body1 card__text"},[e._v("\n      "+e._s(e.text)+"\n    ")]):e._e()]),e._v(" "),e.buttonText?n("div",{staticClass:"card__buttons"},[n("base-button",{staticClass:"card__button outline small",class:[e.cardClasses],on:{click:e.action}},[e._v(e._s(e.buttonText))])],1):e._e()])}),[],!1,null,null,null);n.default=component.exports;installComponents(component,{BaseButton:t(460).default})}}]);