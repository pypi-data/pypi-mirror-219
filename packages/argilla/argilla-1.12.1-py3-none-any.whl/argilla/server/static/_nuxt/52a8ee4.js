(window.webpackJsonp=window.webpackJsonp||[]).push([[62,119],{1018:function(e,n,t){"use strict";t(901)},1019:function(e,n,t){var r=t(80),o=t(94),d=t(95),c=t(96),h=r((function(i){return i[1]})),l=o(d),f=o(c);h.push([e.i,'/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */@font-face{font-family:"raptor_v2_premiumbold";font-style:normal;font-weight:400;src:url('+l+') format("woff2"),url('+f+') format("woff")}/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */.description__text[data-v-441bdf16]{color:rgba(0,0,0,.87);white-space:pre-wrap}.description__text[data-v-441bdf16]:first-letter{text-transform:capitalize}.description__text.--light[data-v-441bdf16]{color:rgba(0,0,0,.37)}',""]),h.locals={},e.exports=h},1060:function(e,n,t){"use strict";t.r(n);var r={props:{datasetDescription:{type:String,required:!0},isColorLight:{type:Boolean,default:!1}},created:function(){this.title="Annotation guidelines"}},o=(t(1018),t(31)),component=Object(o.a)(r,(function(){var e=this,n=e._self._c;return n("div",{staticClass:"description"},[n("h2",{staticClass:"--heading5 --semibold description__title",domProps:{textContent:e._s(e.title)}}),e._v(" "),n("RenderMarkdownBaseComponent",{staticClass:"--body1 description__text",class:{"--light":e.isColorLight},attrs:{markdown:e.datasetDescription}})],1)}),[],!1,null,"441bdf16",null);n.default=component.exports;installComponents(component,{RenderMarkdownBaseComponent:t(843).default})},792:function(e,n,t){var content=t(851);content.__esModule&&(content=content.default),"string"==typeof content&&(content=[[e.i,content,""]]),content.locals&&(e.exports=content.locals);(0,t(81).default)("1f68915d",content,!0,{sourceMap:!1})},843:function(e,n,t){"use strict";t.r(n);t(50),t(97);var r=t(1007),o=t(1008),d=t(241),c=t.n(d),h=t(961);r.marked.use(Object(o.markedHighlight)({langPrefix:"hljs language-",highlight:function(code,e){var n=c.a.getLanguage(e)?e:"plaintext";return c.a.highlight(code,{language:n}).value}}));var l={name:"RenderMarkdownBaseComponent",props:{markdown:{type:String,required:!0}},methods:{cleanMarkdown:function(e){return e.replace(/[^\S\r\n]+$/gm,"")}},created:function(){var e=this.cleanMarkdown(this.markdown),n=r.marked.parse(e,{headerIds:!1,mangle:!1,breaks:!0});this.markdownToHtml=h.sanitize(n)}},f=(t(850),t(31)),component=Object(f.a)(l,(function(){var e=this;return(0,e._self._c)("div",{staticClass:"markdown-render",domProps:{innerHTML:e._s(e.markdownToHtml)}})}),[],!1,null,"07d597f8",null);n.default=component.exports},850:function(e,n,t){"use strict";t(792)},851:function(e,n,t){var r=t(80),o=t(94),d=t(95),c=t(96),h=r((function(i){return i[1]})),l=o(d),f=o(c);h.push([e.i,'/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */@font-face{font-family:"raptor_v2_premiumbold";font-style:normal;font-weight:400;src:url('+l+') format("woff2"),url('+f+') format("woff")}/*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n *//*!\n * coding=utf-8\n * Copyright 2021-present, the Recognai S.L. team.\n *\n * Licensed under the Apache License, Version 2.0 (the "License");\n * you may not use this file except in compliance with the License.\n * You may obtain a copy of the License at\n *\n *     http://www.apache.org/licenses/LICENSE-2.0\n *\n * Unless required by applicable law or agreed to in writing, software\n * distributed under the License is distributed on an "AS IS" BASIS,\n * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\n * See the License for the specific language governing permissions and\n * limitations under the License.\n */.markdown-render[data-v-07d597f8]{white-space:normal;word-break:break-word}.markdown-render[data-v-07d597f8]  hr{width:100%}.markdown-render[data-v-07d597f8]  blockquote{font-style:italic}.markdown-render[data-v-07d597f8]  pre{white-space:pre-wrap;word-break:break-all}.markdown-render[data-v-07d597f8]  code:not(.hljs){background-color:#fffbfa;border-radius:4px;color:#ff675f}.markdown-render[data-v-07d597f8]  a{color:#3e5cc9;word-break:break-all}.markdown-render[data-v-07d597f8]  h1,.markdown-render[data-v-07d597f8]  h2,.markdown-render[data-v-07d597f8]  h3,.markdown-render[data-v-07d597f8]  h4,.markdown-render[data-v-07d597f8]  h5{line-height:1.4em}.markdown-render[data-v-07d597f8]  em,.markdown-render[data-v-07d597f8]  h1,.markdown-render[data-v-07d597f8]  h2,.markdown-render[data-v-07d597f8]  h3,.markdown-render[data-v-07d597f8]  h4,.markdown-render[data-v-07d597f8]  h5,.markdown-render[data-v-07d597f8]  p,.markdown-render[data-v-07d597f8]  strong{margin-bottom:8px;margin-top:0}[data-v-07d597f8]  .hljs{padding:2em!important}[data-v-07d597f8]  .hljs{background-color:#333346;border-radius:5px;color:#fff;font-family:monospace,serif;font-size:13px;font-size:.8125rem;font-weight:500;margin:0;position:relative;text-align:left}[data-v-07d597f8]  .hljs-keyword,[data-v-07d597f8]  .hljs-link,[data-v-07d597f8]  .hljs-literal,[data-v-07d597f8]  .hljs-section,[data-v-07d597f8]  .hljs-selector-tag{color:#3ef070;font-weight:700}[data-v-07d597f8]  .hljs-deletion,[data-v-07d597f8]  .hljs-number,[data-v-07d597f8]  .hljs-quote,[data-v-07d597f8]  .hljs-selector-class,[data-v-07d597f8]  .hljs-selector-id,[data-v-07d597f8]  .hljs-string,[data-v-07d597f8]  .hljs-template-tag,[data-v-07d597f8]  .hljs-type{color:#febf96}[data-v-07d597f8]  .hljs-addition,[data-v-07d597f8]  .hljs-attribute,[data-v-07d597f8]  .hljs-bullet,[data-v-07d597f8]  .hljs-name,[data-v-07d597f8]  .hljs-string,[data-v-07d597f8]  .hljs-symbol,[data-v-07d597f8]  .hljs-template-tag,[data-v-07d597f8]  .hljs-template-variable,[data-v-07d597f8]  .hljs-title,[data-v-07d597f8]  .hljs-type,[data-v-07d597f8]  .hljs-variable{color:#a0c7ee}[data-v-07d597f8]  .hljs-built_in{color:#8fbb62}[data-v-07d597f8]  .hljs-tag,[data-v-07d597f8]  .hljs-tag .hljs-attr,[data-v-07d597f8]  .hljs-tag .hljs-name{color:#c0a5a5}',""]),h.locals={},e.exports=h},901:function(e,n,t){var content=t(1019);content.__esModule&&(content=content.default),"string"==typeof content&&(content=[[e.i,content,""]]),content.locals&&(e.exports=content.locals);(0,t(81).default)("484cb682",content,!0,{sourceMap:!1})}}]);