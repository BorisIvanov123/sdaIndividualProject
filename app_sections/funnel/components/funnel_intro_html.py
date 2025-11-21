FULL_FUNNEL_HTML = """
<div style="padding:16px; background:rgba(255,255,255,0.03);
            border-radius:10px; border:1px solid rgba(255,255,255,0.07);
            margin-bottom:20px;">

<h3 style="margin-top:0;">🪜 Funnel & Exit Behavior</h3>

<p>
    This section analyzes how users progress through the purchase funnel:
    from <strong>initial session</strong>, to <strong>checkout intent</strong>,
    and finally to a <strong>completed order</strong>.
    It highlights where users drop off and how efficiently sessions convert.
</p>

<p><strong>Funnel stages are computed using behavioral flags:</strong></p>

<ul style="margin-left:20px;">
    <li><code>processed = True</code> → user showed purchase intent</li>
    <li><code>converted = True</code> → user completed an order</li>
</ul>

</div>
"""
