" Vim syntax file
" Author:  lightxue
" Email:   bkmgtp@gmail.com
" Version: 0.01
" Website: https://github.com/lightxue/SwissCalc


if exists("b:current_syntax") "{{{
    finish
endif "}}}

if version >= 600 "{{{
    command -nargs=+ HiLink highlight default link <args>
else
    syntax clear
    command -nargs=+ HiLink highlight         link <args>
endif "}}}

"{{{ Pattern

"{{{ Error
syn match scalc_error '^SyntaxError: .*$'
syn match scalc_error '^RuntimeError: .*$'
"}}}

"{{{ String
syn region scalc_string
      \ start=+\z(['"]\)+ end="\z1" skip="\\\\\|\\\z1"
syn region scalc_raw_string
      \ start=+[uU]\=[rR]\z(['"]\)+ end="\z1" skip="\\\\\|\\\z1"
      \ contains=@Spell
syn match scalc_escape    +\\[abfnrtv'"\\]+ contained
syn match scalc_escape    "\\\o\{1,3}" contained
syn match scalc_escape    "\\x\x\{2}" contained
syn match scalc_escape    "\%(\\u\x\{4}\|\\U\x\{8}\)" contained
syn match scalc_escape    "\\N{\a\+\%(\s\a\+\)*}" contained
syn match scalc_escape    "\\$"
"}}}

"{{{ Number
syn match scalc_num    "\<0[oO]\=\o\+[wkmgtpezyWKMGTPEZY]\?\>"
syn match scalc_num    "\<0[xX]\x\+[wkmgtpezyWKMGTPEZY]\?\>"
syn match scalc_num    "\<0[bB][01]\+[wkmgtpezyWKMGTPEZY]\?\>"
syn match scalc_num    "\<\%([1-9]\d*\|0\)[wkmgtpezyWKMGTPEZY]\?\(iB\)\?\>"
syn match scalc_num    "\<\d\+[eE][+-]\=\d\+[wkmgtpezyWKMGTPEZY]\?\(iB\)\?\>"
syn match scalc_num    "\<\d\+\.\%([eE][+-]\=\d\+\)\=\%(\W\|$\)\@=[wkmgtpezyWKMGTPEZY]\?\(iB\)\?\>"
syn match scalc_num    "\%(^\|\W\)\@<=\d*\.\d\+\%([eE][+-]\=\d\+\)\=[wkmgtpezyWKMGTPEZY]\?\(iB\)\?\>"
"}}}

"{{{ Unit
syn match scalc_unit    "亿"
syn match scalc_unit    "万亿"
syn match scalc_unit    "KiB"
syn match scalc_unit    "MiB"
syn match scalc_unit    "GiB"
syn match scalc_unit    "TiB"
syn match scalc_unit    "PiB"
syn match scalc_unit    "EiB"
syn match scalc_unit    "ZiB"
syn match scalc_unit    "YiB"
"}}}

"{{{ Var
syntax match scalc_var "\<e\>"
syntax match scalc_var "\<pi\>"
syntax match scalc_var "\<phi\>"
"}}}

"{{{ Delim
syntax match scalc_delim "(\|)"
"}}}

"{{{ Prompt
if g:scalc_prompt != ''
    silent execute "syn match scalc_prompt '" . g:scalc_prompt . "'"
    HiLink scalc_prompt Type
endif
"}}}

"{{{ Operator
if exists('g:scalc_ops')
    silent execute "syn match scalc_op '" . g:scalc_ops . "'"
    HiLink scalc_op Operator
endif
"}}}

"{{{ Function
if exists('g:scalc_funcs')
    silent execute "syn match scalc_func '" . g:scalc_funcs . "'"
    HiLink scalc_func Function
endif
"}}}

"{{{ Multi-system
syn match  scalc_bin '\<pretty: '
syn match  scalc_bin '\<bin: '
syn match  scalc_oct '\<oct: '
syn match  scalc_dec '\<dec: '
syn region scalc_hex start="\<hex: " end="\X"me=e-1 skip=" "
"}}}

"}}}

"{{{ Highlight

HiLink scalc_bin        Include
HiLink scalc_oct        Define
HiLink scalc_dec        Keyword
HiLink scalc_hex        Number

HiLink scalc_var        Keyword
HiLink scalc_delim      Delimiter

HiLink scalc_string     String
HiLink scalc_raw_string String
HiLink scalc_escape     Special

HiLink scalc_num        Number
HiLink scalc_unit       Number
HiLink scalc_error      ErrorMsg

"}}}

"{{{ Finish

delcommand HiLink

let b:current_syntax = "swisscalc"

"}}}

" vim: foldmethod=marker shiftwidth=4
