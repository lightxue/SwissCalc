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

syntax match scalc_op "+\|-\|\*\|/\|%\|\*\*\|!\|<<\|>>\|&\|\~\||\|\^\|=\|+=\|-=\|\*=\|/=\|%=\|\*\*=\|<<=\|>>=\|&=\||=\|\^="
syntax match scalc_delim "(\|)"

syntax match scalc_float "[0-9]\+\(\.[0-9]\+\)\?\(e[+-]\?[0-9]\+\)\?"
syntax match scalc_hex "0[xX][0-9a-fA-F]\+"
syntax match scalc_oct "0[oO]\?[0-7]\+"
syntax match scalc_bin "0[bB][01]\+"

" TODO string, function, error

if g:SwissCalc_Prompt != ''
    silent execute "syn match scalc_prompt '" . g:SwissCalc_Prompt . "'"
    hi def link scalc Type
endif

if version >= 600
    command -nargs=+ HiLink highlight default link <args>
else
    command -nargs=+ HiLink highlight         link <args>
endif

"Keywords
HiLink vcalcLet         vcalcKeyword
HiLink vcalcKeyword     Keyword

"Functions
HiLink vcalcFuncs       Function

"Operators
HiLink vcalcOps         Operator

"Delimiters
HiLink vcalcDelim       Delimiter

"Directives
HiLink vcalcDirectives  Special

"Numbers
HiLink vcalcDecNum      vcalcNumber
HiLink vcalcHexNum      vcalcNumber
HiLink vcalcOctNum      vcalcNumber
HiLink vcalcNumber      Number

"Errors
HiLink vcalcSynErr      vcalcError
HiLink vcalcParErr      vcalcError
HiLink vcalcError       Error

HiLink scalc_op         Operator
HiLink scalc_delim      Delimiter

HiLink scalc_float      scalc_num
HiLink scalc_hex        scalc_num
HiLink scalc_oct        scalc_num
HiLink scalc_bin        scalc_num
HiLink scalc_num        Number

delcommand HiLink

let b:current_syntax = "swisscalc"
