from rest_framework.views import APIView
from rest_framework.response import Response

class RouteResponseView(APIView):
    def get(self, request, origin, dest):
        polyline = "mtx`Gbmet@~@EJA?B@DBDB@B@BABABE@C?GR?lCKZAAaAEyCCcB?IAo@?QASMyHA[Im@Ki@GOGQEMq@sA[m@OQBI?IAICGEEGCG?[s@Yu@wA{Cw@uAa@q@DMBMAMAMJ[HQh@sA`@g@l@oAX}@Pu@Fe@?e@A[Ie@Qa@W]UU]Qg@[_B{@{As@uB}@m@EmAm@}@e@g@a@w@k@_@[a@_@[[[Km@y@aAcBs@uAc@gAsBcG]}@Uc@o@aAkA_BsAuBm@qAi@kA[_Ak@{Ak@iAg@s@g@k@y@s@aBuAcAeAkBgCa@s@Uc@aAoBk@eBg@iBYkAW{AUiBMkBe@}Gw@qFi@yAo@uA{AuC{G_H}DgDo@o@q@w@m@}@iAsBe@kA_@mAmBsG]_Ao@wAgAkByBoD}@wBk@uBs@uCo@cBeA_B{AiAqAm@yAg@qAw@gAaA_AqAoAgBgCcDoAaBiBcCsByBwDmDQOoAoAe@k@aA}Ao@kA_A{BeCqFqBsCoAqAqAaA}AaAcBu@iBg@mBYqBGoBJw@JiB`@eBp@_B~@yBjBgBhAeAj@mA`@s@LaAN}@DgBE{ASeAYWKSGa@QYQ]Ue@a@{@s@kAwAoBqDIQMSKSMWOUMUOUMSSWOSOSQQMMMMMMOMWSOMSMOIUOWMSIQIQGMEMEOCOESCWESCUC]E_@Es@IQCOASCOAcAG{AKkHg@gAIgk@}CSC]IYGYGe@M[M[Oc@UUOMIKGQOMKMMQQQQOOOQYWk@o@WWKMOMMMOMIIIIGGIGGEQMMIMISIQKQG[MUIQESESEQESCWCUCSCUASAQ?QAU?Q@U@S@S@SBSBSDQDe@JSDQFSHQFOFSJQHWNQHOJQNQJOLOLQNMLMLKJQPQRQVQRQVQVg@t@SXKLILIJKJKJKLMLEBKJYTMJMJo@d@iBbAuEnBmBbAiBjAiBxAcB|AcFvFsAjAiAx@_Af@}Al@oBf@_BVyCJaBIkBMgBWkE_AsCw@kBq@aEuBsA}@kBuAmByAs@o@oCsCsCgD{AgBgDsCyCeBoDsBo@a@yAu@eBcBuA{Ai@u@mAuBgAwB{@yBsAeEmAcCe@}@mAoByAgBaByAs@i@mBgAiFyBqBcAmBoA_D}BkBmAqB_A{@Y{@S}@O}BQ_AA}BF}@J_ANyBj@yDlA{Bj@}B`@aAH_CF_CG_AG_AM{Bg@yBs@y@_@w@a@qGeEoBeAuBs@{@SyBY}BE}BJ_Gn@aCNaCBaCGaAG}B]{Bi@yBs@uBaAsBkAoBwAgB_BcBkBqCgDeBkBkBcBoByAuBkAwBaA{Bu@_ASyBa@wBUwBKwB?yBHgFZqBDsBCqBMqBYaDs@}DcBmBcAuHgEaCoAeB}@{By@uAe@eB]_F_AmDe@gDYyDKqC?kEL_DVyEn@mB`@qCr@q@RsAb@gDrAoB|@wGfDgD~AkDrAmDfAwBf@yB^yBXyBRuF^wBX{@NuBj@y@XoB|@iBjAeBtA}A`BuAhBmAlBmDbHiArBg@t@sAhBm@p@aBzAiBpAoBdAw@ZuBp@y@PqB\\qGp@}Cf@eBd@gBl@eBx@sCbBmCrB{D~CsChBeB|@_DnAmBh@cDp@mD^qCJyA?oAEkBGiBQyDy@mB}@w@a@_Am@c@e@Sq@?_ALu@\\a@^Oh@Db@V^r@Nd@~AdEH^XzAVrAL|@Z`DJpAFtAB`CAdEM`DUvC_@xCi@rCg@vBk@nBcAlCq@tAWj@c@r@i@z@g@h@[Vo@b@k@Zo@b@YV]`@[b@Wh@Ul@YbAWhAQl@M\\IVKNMTONUNa@HO?OEMMY[k@o@cAcA}BwBaEyDq@o@]o@Yo@Wu@]sAQ_AS}AcCmRCOCQASCU?QAQCy@AOAOCWCQCSeAsD_AoCy@aBMWk@y@g@o@_@a@c@e@WWFMlAqDBGDMa@q@iBsCWa@g@u@Ua@o@aAk@{@}AcCOUa@o@ACMQBG@IAGAGCGECDODMJm@Fm@@g@DgABu@?MDuAF_CJa@PWF@HAFCFGBIBI?KAKCIEGEEIQMMEWC]AY?]Ba@@e@"
        
        #TODO backend services

        return Response(
            {
                "polyline":polyline
            }
        )