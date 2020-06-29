import React from 'react'
import numeral from 'numeral'

export function DisplayCount (props) {
    return <span class={props.className}>{numeral(props.children).format("0 a")}</span>
}
