" Vim syntax file
" Author:  lightxue
" Email:   bkmgtp@gmail.com
" Version: 0.01
" Website: https://github.com/lightxue/SwissCalc

if version < 600
    syntax clear
elseif exists("b:current_syntax")
    finish
endif

syn match scalc_error '^SyntaxError: .*$'
syn match scalc_error '^RuntimeError: .*$'

syn region scalc_string
      \ start=+\z(['"]\)+ end="\z1" skip="\\\\\|\\\z1"
syn region scalc_raw_string
      \ start=+[uU]\=[rR]\z(['"]\)+ end="\z1" skip="\\\\\|\\\z1"
      \ contains=@Spell
syn match   scalc_escape    +\\[abfnrtv'"\\]+ contained
syn match   scalc_escape    "\\\o\{1,3}" contained
syn match   scalc_escape    "\\x\x\{2}" contained
syn match   scalc_escape    "\%(\\u\x\{4}\|\\U\x\{8}\)" contained
syn match   scalc_escape    "\\N{\a\+\%(\s\a\+\)*}" contained
syn match   scalc_escape    "\\$"

syn match   scalc_num    "\<0[oO]\=\o\+\>"
syn match   scalc_num    "\<0[xX]\x\+\>"
syn match   scalc_num    "\<0[bB][01]\+\>"
syn match   scalc_num    "\<\%([1-9]\d*\|0\)\>"
syn match   scalc_num    "\<\d\+[eE][+-]\=\d\+\>"
syn match   scalc_num
    \ "\<\d\+\.\%([eE][+-]\=\d\+\)\=\%(\W\|$\)\@="
syn match   scalc_num
    \ "\%(^\|\W\)\@<=\d*\.\d\+\%([eE][+-]\=\d\+\)\=\>"

syntax match scalc_op "+\|-\|\*\|/\|%\|\*\*\|!\|<<\|>>\|&\|\~\||\|\^\|=\|+=\|-=\|\*=\|/=\|%=\|\*\*=\|<<=\|>>=\|&=\||=\|\^="
syntax match scalc_delim "(\|)"

if g:SwissCalc_Prompt != ''
    silent execute "syn match scalc_prompt '" . g:SwissCalc_Prompt . "'"
    hi def link scalc_prompt Label
endif

if version >= 600
    command -nargs=+ HiLink highlight default link <args>
else
    command -nargs=+ HiLink highlight         link <args>
endif


HiLink scalc_op         Operator
HiLink scalc_delim      Delimiter

HiLink scalc_string     String
HiLink scalc_raw_string String
HiLink scalc_escape     Special

HiLink scalc_num        Number
HiLink scalc_error      ErrorMsg

delcommand HiLink

let b:current_syntax = "swisscalc"
