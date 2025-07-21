# Biquad-Filter: Analoge Signalverarbeitung im digitalen Zeitalter

Auch in einer zunehmend digitalen Welt spielt analoge Schaltungstechnik eine zentrale Rolle – insbesondere in der Signalverarbeitung. Physikalische Signale, wie elektromagnetische Wellen bei Funkstrecken, liegen zunächst in analoger Form vor und werden erst später digital verarbeitet. Vor der Digitalisierung durch einen ADC ist daher eine analoge Vorverarbeitung unerlässlich. Sie verbessert den Signal-zu-Rausch-Abstand (SNR) und schützt vor Informationsverlusten.

Ein wichtiger Bestandteil dieser analogen Vorverarbeitung ist die Signalfilterung. Nur durch gezielte Unterdrückung von Rauschen und Störfrequenzen können digitale Systeme das Nutzsignal später korrekt verarbeiten. Die Einhaltung des Nyquist-Kriteriums ist dabei essenziell.

Zentrales Thema dieses Moduls ist der sogenannte **Biquad-Filter** – ein universeller, analoger Filter zweiter Ordnung. Er lässt sich einfach mit wenigen Operationsverstärkern (OPs) realisieren und bietet vielfältige Einsatzmöglichkeiten. Unterschiedliche Kombinationen liefern Hochpass-, Bandpass- oder Tiefpassfunktionen. Für komplexere Filter werden mehrere Biquad-Stufen kaskadiert.

## Zielsetzung

Ziel ist es, den Aufbau und das Verhalten eines analogen Biquad-Filters zu verstehen sowie seine Übertragungsfunktion theoretisch herzuleiten. Besondere Aufmerksamkeit gilt dabei dem **Gütefaktor** \\( Q \\) und dem **Verstärkungsfaktor** \\( H_0 \\).

Nach der theoretischen Betrachtung folgt die praktische Umsetzung auf dem **ASLK-PRO Board**, um Erfahrungen mit den Bauteilwerten (Widerstände, Kondensatoren etc.) zu sammeln. Anschließend wird auf Basis dieser Erkenntnisse eine eigene **Leiterplatte (PCB)** entwickelt.

> **Hinweis:**  
> Der Bericht wurde bewusst in **LaTeX** anstelle von *Quarto* erstellt, da sowohl das **Blockschaltbild (BSB)** als auch die **Schaltpläne** in LaTeX umgesetzt wurden und sich dadurch eine einheitliche Darstellung mit präziser Kontrolle über Formeln und Layout ergab. Falls doch noch Änderung erfolgen und ein Bericht in Quarto erstellt wird, ist dieser unter https://voicid.github.io/Analoge-Schaltungen-ANS/ zu finden.
