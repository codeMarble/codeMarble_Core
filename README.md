# codeMarble_Core

<H3>codeMarble_Core 란?
<H6>'codeMarble'에서 가장 중요한 부분인 정리된 게임 규칙을 적용하고 관리하는 기능을 제공한는 모듈입니다.
<H6>게임 규칙은 '착수 규칙', '착수 후 행동 규칙', '게임 종료 규칙' 3가지로 나누어 분류하며, 사용자 결과를 규칙에 적용하여 게임을 진행합니다.
<H6>그리고 사용자 코드를 관리(컴파일, 실행)에 필요한 기능도 함께 제공하고 있습니다.
-

<H3>요구 규칙 및 데이터 형태

<H6> placementRule : 착수 규칙. 돌을 추가한는 방식(1)인지 돌을 옮기는 방식인지(2) 설정한다. {data type : int}
<H6> placementOption : 착수 규칙의 추가 옵션. 착수 규칙에 따라 이웃 돌과 연결 규칙이나 이동 방향/크기를 설정한다. {data type : [[],[],[]]/int}
<H6> existRule : 돌이 중복되는 경우 필요한 규칙을 설정. 자신의 돌, 상대의 돌, 다른 오브젝트인 경우 3가지로 구분한다. {data type : [int, int, int]}
<H6> existOption : existRule에 추가할 옵션을 설정한다. 규칙 순서는 existRule과 동일하다. {data type : [int, int, int]}
<H6> actionRule : 착수 후 착수한 돌과 그 주변에 일어날 행동을 설정. 제거(1)와 변경(2)이 있다. {data type : int}
<H6> actionOption : actionRule이 반영되는 방향 및 크기 또는 적용 방법을 설정할 수 있다. {data type : [int, int]}
<H6> endingRule : 게임이 종료되는 규칙을 설정. 특정 돌이 제거되는 규칙(1), 오목 규칙(2), 다수(다득점) 규칙(3)이 있다. {data type : int}
<H6> endingOption : 종료 규칙에 추가되는 옵션을 설정. 오목과 같은 규칙에 필요한 방향과 크기 등을 설정한다. {data type : [int, int]}

-
<H4> 게임 규칙은 각 규칙과 추가로 필요한 옵션들이 숫자로 정리되어 있어 구성하는데 어려움이 있을 수 있습니다.
<H4> 이 경우 'Maker'를 이용하면 쉽게 게임을 만들수 있습니다.
                    
